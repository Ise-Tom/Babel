-- Synthetic local-state experiment. Not an AD directory, authentication service or stable disk format.
CREATE SCHEMA babel_lab;
REVOKE ALL ON SCHEMA babel_lab FROM PUBLIC;

CREATE TABLE babel_lab.state (
    singleton boolean PRIMARY KEY CHECK (singleton),
    schema_version integer NOT NULL CHECK (schema_version = 1),
    invocation_id uuid NOT NULL,
    last_usn bigint NOT NULL CHECK (last_usn >= 0)
);
INSERT INTO babel_lab.state VALUES (true, 1, '00000000-0000-4000-8000-000000000002', 0);

-- This allow/deny switch is a test input, not principal authentication or Windows ACL semantics.
CREATE TABLE babel_lab.actors (actor_id uuid PRIMARY KEY, active boolean NOT NULL);
INSERT INTO babel_lab.actors VALUES ('00000000-0000-4000-8000-000000000001', true);

CREATE TABLE babel_lab.objects (
    object_id uuid PRIMARY KEY,
    synthetic_sid text UNIQUE NOT NULL
        CHECK (synthetic_sid ~ '^S-1-5-21-100-200-300-[1-9][0-9]{3,8}$'),
    synthetic_label text COLLATE "C" UNIQUE NOT NULL
        CHECK (synthetic_label ~ '^[a-z][a-z0-9-]{0,31}$'),
    object_version bigint NOT NULL CHECK (object_version > 0)
);
CREATE TABLE babel_lab.journal (
    local_usn bigint PRIMARY KEY CHECK (local_usn > 0),
    actor_id uuid NOT NULL REFERENCES babel_lab.actors,
    object_id uuid NOT NULL REFERENCES babel_lab.objects,
    operation text NOT NULL CHECK (operation IN ('create', 'rename'))
);
CREATE TABLE babel_lab.audit_intent (
    local_usn bigint PRIMARY KEY REFERENCES babel_lab.journal,
    actor_id uuid NOT NULL REFERENCES babel_lab.actors
);
CREATE TABLE babel_lab.receipts (
    actor_id uuid NOT NULL REFERENCES babel_lab.actors,
    request_id uuid NOT NULL,
    payload jsonb NOT NULL,
    local_usn bigint NOT NULL REFERENCES babel_lab.journal,
    PRIMARY KEY (actor_id, request_id)
);

CREATE FUNCTION babel_lab.immutable_identity() RETURNS trigger
LANGUAGE plpgsql SET search_path = pg_catalog, babel_lab AS $$
BEGIN
    IF NEW.object_id IS DISTINCT FROM OLD.object_id
       OR NEW.synthetic_sid IS DISTINCT FROM OLD.synthetic_sid THEN
        RAISE EXCEPTION 'immutable synthetic identity' USING ERRCODE = '23000';
    END IF;
    RETURN NEW;
END;
$$;
CREATE TRIGGER immutable_identity BEFORE UPDATE ON babel_lab.objects
FOR EACH ROW EXECUTE FUNCTION babel_lab.immutable_identity();

CREATE FUNCTION babel_lab.mutate(
    actor uuid, request uuid, operation text, object_guid uuid,
    sid text, label text, expected_version bigint
) RETURNS bigint
LANGUAGE plpgsql SET search_path = pg_catalog, babel_lab AS $$
DECLARE
    actor_active boolean;
    operation_payload jsonb;
    previous_payload jsonb;
    previous_usn bigint;
    assigned_usn bigint;
    changed_version bigint;
BEGIN
    IF current_setting('fsync') <> 'on'
       OR current_setting('full_page_writes') <> 'on'
       OR current_setting('synchronous_commit') <> 'on' THEN
        RAISE EXCEPTION 'unsafe durability settings' USING ERRCODE = '55000';
    END IF;
    -- The first experiment deliberately serializes all writers before other mutation locks.
    PERFORM 1 FROM babel_lab.state WHERE singleton FOR UPDATE;
    SELECT active INTO actor_active FROM babel_lab.actors WHERE actor_id = actor FOR SHARE;
    IF NOT coalesce(actor_active, false) THEN
        RAISE EXCEPTION 'inactive test actor' USING ERRCODE = '42501';
    END IF;
    IF operation IS NULL OR operation NOT IN ('create', 'rename')
       OR label IS NULL OR label !~ '^[a-z][a-z0-9-]{0,31}$'
       OR sid IS NULL OR sid !~ '^S-1-5-21-100-200-300-[1-9][0-9]{3,8}$'
       OR expected_version IS NULL OR expected_version < 0
       OR object_guid IS NULL OR request IS NULL THEN
        RAISE EXCEPTION 'invalid synthetic operation' USING ERRCODE = '22023';
    END IF;
    -- Exact bounded payload equality avoids relying on an unqualified digest/canonicalization format.
    operation_payload := jsonb_build_array(operation, object_guid, sid, label, expected_version);
    SELECT payload, local_usn INTO previous_payload, previous_usn
        FROM babel_lab.receipts WHERE actor_id = actor AND request_id = request;
    IF FOUND THEN
        IF previous_payload <> operation_payload THEN
            RAISE EXCEPTION 'request identity reused for another operation' USING ERRCODE = '22023';
        END IF;
        RETURN previous_usn;
    END IF;
    IF operation = 'create' THEN
        IF expected_version <> 0 THEN
            RAISE EXCEPTION 'invalid creation version' USING ERRCODE = '40001';
        END IF;
        INSERT INTO babel_lab.objects VALUES (object_guid, sid, label, 1);
    ELSE
        UPDATE babel_lab.objects
            SET synthetic_label = label, object_version = object_version + 1
            WHERE object_id = object_guid AND synthetic_sid = sid AND object_version = expected_version
            RETURNING object_version INTO changed_version;
        IF NOT FOUND THEN
            RAISE EXCEPTION 'missing or stale synthetic object' USING ERRCODE = '40001';
        END IF;
    END IF;
    UPDATE babel_lab.state SET last_usn = last_usn + 1
        WHERE singleton AND last_usn < 9223372036854775807 RETURNING last_usn INTO assigned_usn;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'local journal exhausted' USING ERRCODE = '54000';
    END IF;
    INSERT INTO babel_lab.journal VALUES (assigned_usn, actor, object_guid, operation);
    INSERT INTO babel_lab.audit_intent VALUES (assigned_usn, actor);
    INSERT INTO babel_lab.receipts VALUES (actor, request, operation_payload, assigned_usn);
    RETURN assigned_usn;
END;
$$;
REVOKE ALL ON ALL TABLES IN SCHEMA babel_lab FROM PUBLIC;
REVOKE ALL ON ALL FUNCTIONS IN SCHEMA babel_lab FROM PUBLIC;
