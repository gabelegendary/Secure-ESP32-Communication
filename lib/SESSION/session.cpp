#include "session.h"
#include "session_constants.h"
#include "serial_communication.h"
#include <Arduino.h>
#include <mbedtls/aes.h>
#include <mbedtls/md.h>
#include <mbedtls/pk.h>
#include <mbedtls/entropy.h>
#include <mbedtls/ctr_drbg.h>

// Initialize cryptographic contexts
static mbedtls_aes_context aes_ctx;
static mbedtls_md_context_t hmac_ctx;
static mbedtls_pk_context public_key_client;
static mbedtls_pk_context public_key_server;
static mbedtls_entropy_context entropy;
static mbedtls_ctr_drbg_context ctr_drbg;

static uint8_t aes_key[AES_SIZE] = {0};
static uint8_t enc_iv[AES_BLOCK_SIZE] = {0};
static uint8_t dec_iv[AES_BLOCK_SIZE] = {0};

// Predefined HMAC key for message authentication
static const uint8_t hmac_key[HMAC_SIZE] = {
    0x29, 0x49, 0xde, 0xc2, 0x3e, 0x1e, 0x34, 0xb5, 0x2d, 0x22, 0xb5,
    0xba, 0x4c, 0x34, 0x23, 0x3a, 0x9d, 0x3f, 0xe2, 0x97, 0x14, 0xbe,
    0x24, 0x62, 0x81, 0x0c, 0x86, 0xb1, 0xf6, 0x92, 0x54, 0xd6};

void session_init(void)
{
    initialize_serial(); // Initialize serial communication

    // Initialize HMAC context with SHA-256
    mbedtls_md_init(&hmac_ctx);
    assert(0 == mbedtls_md_setup(&hmac_ctx, mbedtls_md_info_from_type(MBEDTLS_MD_SHA256), 1));

    // Initialize AES context
    mbedtls_aes_init(&aes_ctx);

    uint8_t initial[AES_SIZE] = {0};
    mbedtls_entropy_init(&entropy);   // Initialize entropy context
    mbedtls_ctr_drbg_init(&ctr_drbg); // Initialize DRBG context

    // Generate initial random values
    for (size_t i = 0; i < sizeof(initial); i++)
    {
        initial[i] = random(0x100);
    }
    assert(0 == mbedtls_ctr_drbg_seed(&ctr_drbg, mbedtls_entropy_func, &entropy, initial, sizeof(initial)));
}

void server_receive_and_verify_key(void)
{
    uint8_t client_key_buf[KEY_SIZE + HMAC_SIZE] = {0};
    size_t len = receive_data(client_key_buf, sizeof(client_key_buf));

    if (len == 0)
    {
        Serial.println("No data received.");
        return;
    }

    size_t hmac_offset = len - HMAC_SIZE;

    Serial.print("Received Client Key Buffer: ");
    for (size_t i = 0; i < sizeof(client_key_buf); ++i)
    {
        Serial.printf("%02X", client_key_buf[i]);
    }
    Serial.println();

    uint8_t rec_hmac[32] = {0};
    assert(0 == mbedtls_md_hmac_starts(&hmac_ctx, hmac_key, HMAC_SIZE));
    assert(0 == mbedtls_md_hmac_update(&hmac_ctx, client_key_buf, hmac_offset));
    assert(0 == mbedtls_md_hmac_finish(&hmac_ctx, rec_hmac));

    if (memcmp(rec_hmac, client_key_buf + hmac_offset, HMAC_SIZE) != 0)
    {
        Serial.println("HMAC verification failed");
        return;
    }
    else
    {
        Serial.println("HMAC verification passed");
        Serial.print("Received Client Public Key: ");
        for (size_t i = 0; i < hmac_offset; ++i)
        {
            Serial.printf("%02X", client_key_buf[i]);
        }
        Serial.println();
    }

    // Initialize RSA context for server
    mbedtls_pk_init(&public_key_server);
    assert(0 == mbedtls_pk_setup(&public_key_server, mbedtls_pk_info_from_type(MBEDTLS_PK_RSA)));

    // Generate RSA key pair
    int ret = mbedtls_rsa_gen_key(mbedtls_pk_rsa(public_key_server), mbedtls_ctr_drbg_random, &ctr_drbg, RSA_SIZE * 8, EXPONENT);
    if (ret != 0)
    {
        Serial.printf("Failed to generate RSA key pair: %d\n", ret);
        return;
    }

    uint8_t server_key_buf[KEY_SIZE] = {0};
    size_t olen = 0;
    mbedtls_pk_write_pubkey_der(&public_key_server, server_key_buf, sizeof(server_key_buf));

    // Encrypt the server's public key
    uint8_t encrypted_msg[MSG_SIZE] = {0};
    mbedtls_aes_crypt_ecb(&aes_ctx, MBEDTLS_AES_ENCRYPT, server_key_buf, encrypted_msg);

    send_data(encrypted_msg, sizeof(encrypted_msg));
}
