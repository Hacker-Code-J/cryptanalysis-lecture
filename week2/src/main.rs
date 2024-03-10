use std::env;
use week2::caesar::{caesar_encrypt, caesar_decrypt}; // Assuming your package is named 'caesar_cipher'

// cargo build --release
// ./target/release/week2 encrypt 3 'Hello, World!'
// cargo run --release -- encrypt 3 'Hello, World!'
// ./target/release/week2 decrypt 3 'Khoor, Zruog!'

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 4 {
        println!("Usage: {} (encrypt|decrypt) <key> <message>", args[0]);
        return;
    }

    let command = &args[1];
    let key: usize = match args[2].parse() {
        Ok(num) => num,
        Err(_) => {
            println!("Please provide a valid number for the key.");
            return;
        },
    };
    let message = &args[3];

    match command.as_str() {
        "encrypt" => {
            let encrypted = caesar_encrypt(key, message);
            println!("Encrypted Message: {}", encrypted);
        },
        "decrypt" => {
            let decrypted = caesar_decrypt(key, message);
            println!("Decrypted Message: {}", decrypted);
        },
        _ => {
            println!("Invalid command. Use 'encrypt' or 'decrypt'.");
        },
    }
}