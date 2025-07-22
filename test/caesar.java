//WRITE A PROGRAM TO IMPLEMENT ANY CLASSIC CRYPTOGRAPHIC TECHNIQUE
import java.util.Scanner;

public class caesar {

    public static String encrypt(String str, int key) {
    StringBuilder encrypted_text = new StringBuilder();
    for (int i = 0; i < str.length(); i++) {
        char c = str.charAt(i);
        if (Character.isLetter(c)) {
            int base = Character.isUpperCase(c) ? 'A' : 'a';
            encrypted_text.append((char) (((c - base + key) % 26) + base));
        } else if (Character.isDigit(c)) {
            encrypted_text.append((char) (((c - '0' + key) % 10) + '0'));
        } else {
            encrypted_text.append(c);
        }
    }
    return encrypted_text.toString();
}

public static String decrypt(String str, int key) {
    StringBuilder decrypted_text = new StringBuilder();
    for (int i = 0; i < str.length(); i++) {
        char c = str.charAt(i);
        if (Character.isLetter(c)) {
            int base = Character.isUpperCase(c) ? 'A' : 'a';
            decrypted_text.append((char) (((c - base - key + 26) % 26) + base));
        } else if (Character.isDigit(c)) {
            decrypted_text.append((char) (((c - '0' - key + 10) % 10) + '0'));
        } else {
            decrypted_text.append(c);
        }
    }
    return decrypted_text.toString();
}

    public static void main(String[] args) {
        @SuppressWarnings("resource")
        Scanner sc = new Scanner(System.in);
        
        System.out.print("Enter plain text : ");
        String plain_text = sc.nextLine();
        
	System.out.print("Enter key value : ");
	int key = sc.nextInt();
        
   
        String enc = encrypt(plain_text, key);
        System.out.println("Encrypted Text is : "+enc);
        String dec = decrypt(enc,key);
        System.out.println("Decrypted Text is : "+dec);
    }
}