pub fn caesar_encrypt(key: usize, plain_msg: &str) -> String {
    let up_alphabet: Vec<char> = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".chars().collect();
    let low_alphabet: Vec<char> = "abcdefghijklmnopqrstuvwxyz".chars().collect();
    let mut cipher_msg = String::new();

    for symbol in plain_msg.chars() {
        if let Some(pos) = up_alphabet.iter().position(|&c| c == symbol) {
            let trans_idx = (pos + key) % up_alphabet.len();
            cipher_msg.push(up_alphabet[trans_idx]);
        } else if let Some(pos) = low_alphabet.iter().position(|&c| c == symbol) {
            let trans_idx = (pos + key) % low_alphabet.len();
            cipher_msg.push(low_alphabet[trans_idx]);
        } else {
            cipher_msg.push(symbol);
        }
    }

    cipher_msg
}

pub fn caesar_decrypt(key: usize, cipher_msg: &str) -> String {
    let up_alphabet: Vec<char> = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".chars().collect();
    let low_alphabet: Vec<char> = "abcdefghijklmnopqrstuvwxyz".chars().collect();
    let mut recovered_msg = String::new();

    for symbol in cipher_msg.chars() {
        if let Some(pos) = up_alphabet.iter().position(|&c| c == symbol) {
            let trans_idx = (pos + up_alphabet.len() - key) % up_alphabet.len();
            recovered_msg.push(up_alphabet[trans_idx]);
        } else if let Some(pos) = low_alphabet.iter().position(|&c| c == symbol) {
            let trans_idx = (pos + low_alphabet.len() - key) % low_alphabet.len();
            recovered_msg.push(low_alphabet[trans_idx]);
        } else {
            recovered_msg.push(symbol);
        }
    }

    recovered_msg
}