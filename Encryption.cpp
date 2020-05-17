//
//

#include <iostream>


#include <openssl/aes.h>
#include <openssl/evp.h>
#include <sstream>


#define AES_KEYLENGTH 128
#define AES_BLOCK_SIZE 16

// a simple hex-print routine. could be modified to print 16 bytes-per-line
static void hex_print(const void* pv, size_t len)
{
    const unsigned char* p = (const unsigned char*)pv;
    if (NULL == pv)
        printf("NULL");
    else
    {
        size_t i = 0;
        for (; i < len; ++i)
            printf("%02X ", *p++);
    }
    printf("\n");
}






int main()
{
        size_t inputslength = 0;

        //TAKE CARE AT LENGHT
        unsigned char Token[] = "Token to encrypt";

       unsigned char zigBeeLinkKey[] = "ZTk0YTU011111111";
       int sourceID = 0x12345678;
       unsigned char iv[] = "0f9387b3f94bf";

       inputslength = strlen((char*)zigBeeLinkKey) + 1;

       unsigned char nonce[13];
       char sourceIDInBytes[4];

       sourceIDInBytes[0] = sourceID & 0x000000ff;
       sourceIDInBytes[1] = (sourceID & 0x0000ff00) >> 8;
       sourceIDInBytes[2] = (sourceID & 0x00ff0000) >> 16;
       sourceIDInBytes[3] = (sourceID & 0xff000000) >> 24;

       for (int i = 0; i < 3; i++)
       {
           for (int j = 0; j < 4; j++)
           {
               nonce[4 * i + j] = sourceIDInBytes[j];
           }
       }
       nonce[12] = 0x05;

        unsigned char* aes_input = new unsigned char[inputslength];
        memset((void*)aes_input, 0, inputslength / 8);
        strcpy((char*)aes_input, (const char*)Token);


        // buffers for encryption and decryption
        const size_t encslength = ((inputslength + AES_BLOCK_SIZE) / AES_BLOCK_SIZE) * AES_BLOCK_SIZE;
        unsigned char* enc_out = new unsigned char[encslength];
        unsigned char* dec_out = new unsigned char[inputslength*3];
        memset(enc_out, 0, sizeof(enc_out));
        memset(dec_out, 0, sizeof(dec_out));

        EVP_CIPHER_CTX* ctx;
        int outlen, tmplen;

        ctx = EVP_CIPHER_CTX_new();

        /* Set cipher type and mode */
        EVP_EncryptInit_ex(ctx, EVP_aes_128_ccm(), NULL, NULL, NULL);

        /* Set nonce length if default 96 bits is not appropriate */
        EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_AEAD_SET_IVLEN, sizeof(nonce), NULL);

        //  /* Set tag length */
        //  EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_AEAD_SET_TAG, sizeof(ccm_tag), NULL);

        /* Initialise key and IV */
        EVP_EncryptInit_ex(ctx, NULL, NULL, zigBeeLinkKey, nonce);

        /* Encrypt plaintext: can only be called once */
        EVP_EncryptUpdate(ctx, enc_out, &outlen, Token, sizeof(Token));
        enc_out[outlen - 1] = '\0';

        EVP_CIPHER_CTX_free(ctx);

        printf("original:\t");
        hex_print(aes_input, strlen((const char*)aes_input));
        printf("encrypt:\t");
        hex_print(enc_out, strlen((const char*)enc_out));


        std::stringstream ss;
        for (int i = 0; i < encslength; i++)
        {
            ss << enc_out[i];
        }

        delete[] aes_input;
        delete[] enc_out;
        delete[] dec_out;


        return 0;

}

