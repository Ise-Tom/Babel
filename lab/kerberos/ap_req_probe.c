/* Disposable MIT krb5 qualification probe. Synthetic realm only. */
#include <krb5.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

static void die(krb5_context ctx, const char *where, krb5_error_code code) {
    const char *message = krb5_get_error_message(ctx, code);
    fprintf(stderr, "%s: %s (%ld)\n", where, message, (long)code);
    krb5_free_error_message(ctx, message);
    exit(2);
}

static krb5_keytab_entry key(krb5_context ctx, krb5_keytab tab,
                             const char *name, krb5_enctype enctype) {
    krb5_principal principal = NULL;
    krb5_keytab_entry entry;
    krb5_error_code code;
    memset(&entry, 0, sizeof(entry));
    code = krb5_parse_name(ctx, name, &principal);
    if (code) die(ctx, "parse key principal", code);
    code = krb5_kt_get_entry(ctx, tab, principal, 0, enctype, &entry);
    krb5_free_principal(ctx, principal);
    if (code) die(ctx, "read keytab entry", code);
    return entry;
}

int main(int argc, char **argv) {
    krb5_context ctx = NULL;
    krb5_auth_context client_auth = NULL, server_auth = NULL, replay_auth = NULL, wrong_auth = NULL;
    krb5_ccache cache = NULL;
    krb5_keytab tab = NULL;
    krb5_principal expected = NULL, wrong = NULL;
    krb5_ticket *ticket = NULL, *duplicate = NULL;
    krb5_keytab_entry server_key, kdc_key;
    krb5_pac pac = NULL;
    krb5_pac tampered_pac = NULL;
    krb5_authdata **pac_data = NULL;
    unsigned char *tampered = NULL;
    krb5_data request = {0};
    krb5_error_code code, replay_code, wrong_code, pac_code, client_code;
    const char *mode;
    if (argc != 7) {
        fprintf(stderr, "usage: %s mode service host expected wrong keytab\n", argv[0]);
        return 2;
    }
    mode = argv[1];
    if ((code = krb5_init_context(&ctx))) die(ctx, "init", code);
    if ((code = krb5_cc_default(ctx, &cache))) die(ctx, "cache", code);
    if ((code = krb5_kt_resolve(ctx, argv[6], &tab))) die(ctx, "keytab", code);
    if ((code = krb5_parse_name(ctx, argv[4], &expected))) die(ctx, "server name", code);
    if ((code = krb5_parse_name(ctx, argv[5], &wrong))) die(ctx, "wrong name", code);
    code = krb5_mk_req(ctx, &client_auth, 0, argv[2], argv[3], NULL, cache, &request);
    if (code) die(ctx, "mk_req", code);
    if (strcmp(mode, "expired") == 0) sleep(5);
    code = krb5_rd_req(ctx, &server_auth, &request, expected, tab, NULL, &ticket);
    if (strcmp(mode, "expired") == 0) {
        printf("expired_rd_req=%ld\n", (long)code);
        return code == KRB5KRB_AP_ERR_TKT_EXPIRED ? 0 : 1;
    }
    if (code) die(ctx, "rd_req", code);
    printf("accepted_enctype=%d\n", ticket->enc_part.enctype);
    wrong_code = krb5_rd_req(ctx, &wrong_auth, &request, wrong, tab, NULL, NULL);
    printf("wrong_service_rd_req=%ld\n", (long)wrong_code);
    if (wrong_code != KRB5KRB_AP_ERR_NOT_US) return 1;
    replay_code = krb5_rd_req(ctx, &replay_auth, &request, expected, tab, NULL, &duplicate);
    printf("replay_rd_req=%ld\n", (long)replay_code);
    if (replay_code != KRB5KRB_AP_ERR_REPEAT) return 1;
    server_key = key(ctx, tab, argv[4], ticket->enc_part.enctype);
    /* The KDC checksum uses the krbtgt key, which need not match service etype. */
    kdc_key = key(ctx, tab, "krbtgt/BABEL.TEST@BABEL.TEST",
                  ENCTYPE_AES256_CTS_HMAC_SHA1_96);
    pac_code = krb5_kdc_verify_ticket(ctx, ticket->enc_part2, expected,
                                      &server_key.key, &kdc_key.key, &pac);
    printf("pac_signature_verify=%ld\n", (long)pac_code);
    if (pac_code) return 1;
    if (strcmp(mode, "missing") == 0) {
        printf("pac_present=%d\n", pac != NULL);
        return pac == NULL ? 0 : 1;
    }
    if (pac == NULL) return 1;
    client_code = krb5_pac_verify(ctx, pac, ticket->enc_part2->times.authtime,
                                  ticket->enc_part2->client, NULL, NULL);
    printf("pac_client_verify=%ld\n", (long)client_code);
    if (client_code) return 1;
    /* A wrong principal must never turn a verified PAC into authority. */
    client_code = krb5_pac_verify(ctx, pac, ticket->enc_part2->times.authtime,
                                  wrong, NULL, NULL);
    printf("pac_wrong_client_verify=%ld\n", (long)client_code);
    if (client_code == 0) return 1;
    code = krb5_find_authdata(ctx, ticket->enc_part2->authorization_data,
                              NULL, KRB5_AUTHDATA_WIN2K_PAC, &pac_data);
    if (code || pac_data == NULL || pac_data[0] == NULL || pac_data[1] != NULL ||
        pac_data[0]->length < 32) return 1;
    tampered = malloc(pac_data[0]->length);
    if (tampered == NULL) return 2;
    memcpy(tampered, pac_data[0]->contents, pac_data[0]->length);
    tampered[pac_data[0]->length - 1] ^= 1;
    code = krb5_pac_parse(ctx, tampered, pac_data[0]->length, &tampered_pac);
    if (code == 0) {
        code = krb5_pac_verify(ctx, tampered_pac,
                               ticket->enc_part2->times.authtime,
                               ticket->enc_part2->client,
                               &server_key.key, &kdc_key.key);
    }
    printf("tampered_pac_verify=%ld\n", (long)code);
    if (code == 0) return 1;
    free(tampered);
    if (tampered_pac != NULL) krb5_pac_free(ctx, tampered_pac);
    krb5_free_authdata(ctx, pac_data);
    krb5_pac_free(ctx, pac);
    krb5_kt_free_entry(ctx, &server_key);
    krb5_kt_free_entry(ctx, &kdc_key);
    krb5_free_ticket(ctx, ticket);
    krb5_free_data_contents(ctx, &request);
    krb5_auth_con_free(ctx, client_auth);
    krb5_auth_con_free(ctx, server_auth);
    krb5_kt_close(ctx, tab);
    krb5_cc_close(ctx, cache);
    krb5_free_principal(ctx, expected);
    krb5_free_principal(ctx, wrong);
    krb5_free_context(ctx);
    return 0;
}
