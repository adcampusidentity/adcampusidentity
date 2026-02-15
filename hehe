package main

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"crypto/sha256"
	"encoding/base64"
	"fmt"
	"io"
)

func main() {
	// Thông tin người dùng và địa chỉ email
	email := "admin@campusidentity.tech"
	fmt.Println("User Email:", email)

	// Mã hóa AES
	plaintext := []byte("This is a secret message.")

	// Tạo key AES từ SHA256 của email
	key := sha256.Sum256([]byte(email))
	ciphertext, err := encryptAES(plaintext, key[:])
	if err != nil {
		fmt.Println("Error encrypting:", err)
		return
	}

	// In ra dữ liệu đã mã hóa dưới dạng base64
	fmt.Println("Encrypted text (base64):", base64.StdEncoding.EncodeToString(ciphertext))
}

// Hàm mã hóa AES
func encryptAES(plaintext []byte, key []byte) ([]byte, error) {
	block, err := aes.NewCipher(key)
	if err != nil {
		return nil, err
	}

	// Tạo IV (Initialization Vector)
	ciphertext := make([]byte, aes.BlockSize+len(plaintext))
	iv := ciphertext[:aes.BlockSize]
	_, err = io.ReadFull(rand.Reader, iv)
	if err != nil {
		return nil, err
	}

	// Mã hóa
	stream := cipher.NewCFBEncrypter(block, iv)
	stream.XORKeyStream(ciphertext[aes.BlockSize:], plaintext)

	return ciphertext, nil
}
