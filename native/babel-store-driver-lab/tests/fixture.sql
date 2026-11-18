CREATE SCHEMA driver_lab;
CREATE TABLE driver_lab.records(id bigint PRIMARY KEY, label text NOT NULL UNIQUE CHECK(octet_length(label)<=256));
CREATE TABLE driver_lab.journal(id bigint PRIMARY KEY REFERENCES driver_lab.records(id) DEFERRABLE INITIALLY DEFERRED);
GRANT USAGE ON SCHEMA driver_lab TO babel_driver_lab;
GRANT SELECT,INSERT,UPDATE,DELETE ON ALL TABLES IN SCHEMA driver_lab TO babel_driver_lab;

-- The existing SQL experiment owns all atomic state/journal/audit/receipt semantics.
-- This wrapper restricts the driver's typed path to that function, not raw table access.
CREATE FUNCTION driver_lab.apply(actor text, request text, operation text, object_guid text,
                                 sid text, label text, expected bigint) RETURNS bigint
LANGUAGE sql SECURITY DEFINER SET search_path = pg_catalog, babel_lab AS $$
    SELECT babel_lab.mutate(actor::uuid, request::uuid, operation, object_guid::uuid, sid, label, expected);
$$;
REVOKE ALL ON FUNCTION driver_lab.apply(text,text,text,text,text,text,bigint) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION driver_lab.apply(text,text,text,text,text,text,bigint) TO babel_driver_lab;

-- Explicit fixture projections; direct access to the experiment tables stays denied.
CREATE FUNCTION driver_lab.effects(object_guid text) RETURNS TABLE(objects bigint, journal bigint, audit bigint, receipts bigint)
LANGUAGE sql SECURITY DEFINER SET search_path = pg_catalog, babel_lab AS $$
 SELECT (SELECT count(*) FROM babel_lab.objects WHERE object_id=object_guid::uuid),
        (SELECT count(*) FROM babel_lab.journal WHERE object_id=object_guid::uuid),
        (SELECT count(*) FROM babel_lab.audit_intent WHERE local_usn IN (SELECT local_usn FROM babel_lab.journal WHERE object_id=object_guid::uuid)),
        (SELECT count(*) FROM babel_lab.receipts WHERE local_usn IN (SELECT local_usn FROM babel_lab.journal WHERE object_id=object_guid::uuid));
$$;
REVOKE ALL ON FUNCTION driver_lab.effects(text) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION driver_lab.effects(text) TO babel_driver_lab;

-- A controlled lock barrier for caller-cancellation tests, not a product operation.
CREATE OR REPLACE FUNCTION driver_lab.apply(actor text, request text, operation text, object_guid text,
                                 sid text, label text, expected bigint) RETURNS bigint
LANGUAGE plpgsql SECURITY DEFINER SET search_path = pg_catalog, babel_lab AS $$
BEGIN
    IF label='wait-mutation' THEN PERFORM pg_advisory_xact_lock(882204); END IF;
    RETURN babel_lab.mutate(actor::uuid, request::uuid, operation, object_guid::uuid, sid, label, expected);
END;
$$;

CREATE FUNCTION driver_lab.set_actor_active(actor text, enabled boolean) RETURNS void
LANGUAGE sql SECURITY DEFINER SET search_path = pg_catalog, babel_lab AS $$
 UPDATE babel_lab.actors SET active=enabled WHERE actor_id=actor::uuid;
$$;
REVOKE ALL ON FUNCTION driver_lab.set_actor_active(text,boolean) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION driver_lab.set_actor_active(text,boolean) TO babel_driver_lab;
