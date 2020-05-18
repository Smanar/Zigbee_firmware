//
//

#include <iostream>


#include <openssl/aes.h>
#include <openssl/evp.h>
#include <sstream>


#define AES_KEYLENGTH 128
#define AES_BLOCK_SIZE 16

const unsigned char zigBeeLinkKey[] = { 0x5A, 0x69, 0x67, 0x42, 0x65, 0x65, 0x41, 0x6C, 0x6C, 0x69, 0x61, 0x6E, 0x63, 0x65, 0x30, 0x39 };


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


unsigned char * encryptSecurityKey(int sourceID, unsigned char *securityKey) {

	unsigned char nonce[13];
	char sourceIDInBytes[4];

	size_t inputslength = strlen((char*)securityKey) ;

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

	// buffers for encryption and decryption
	const size_t encslength = ((inputslength + AES_BLOCK_SIZE) / AES_BLOCK_SIZE) * AES_BLOCK_SIZE;
	unsigned char* EncryptedKey = new unsigned char[encslength];
	memset(EncryptedKey, 0, sizeof(EncryptedKey));

	EVP_CIPHER_CTX* ctx;
	int outlen;

	ctx = EVP_CIPHER_CTX_new();

	/* Set cipher type and mode */
	EVP_EncryptInit_ex(ctx, EVP_aes_128_ccm(), NULL, NULL, NULL);

	/* Set nonce length if default 96 bits is not appropriate */
	EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_AEAD_SET_IVLEN, sizeof(nonce), NULL);

	/* Initialise key and IV */
	EVP_EncryptInit_ex(ctx, NULL, NULL, zigBeeLinkKey, nonce);

	/* Encrypt plaintext: can only be called once */
	EVP_EncryptUpdate(ctx, EncryptedKey, &outlen, securityKey, (int)inputslength);
	EncryptedKey[outlen] = '\0';

	EVP_CIPHER_CTX_free(ctx);

	return EncryptedKey;
}



int main()
{

	//from deconz
	unsigned char key[] = "ZTk0YTU011111111";
	int gpdSrcId = 0x12345678;

	//Fonction to get key encrypted
	unsigned char* EncryptedKey = encryptSecurityKey(gpdSrcId, key);

	printf("encrypt:\t");
	hex_print(EncryptedKey, strlen((const char*)EncryptedKey));

	return 0;

}

