use std::collections::HashMap;

fn ic(msg: &str) -> f64 {
    let up_alphabet: Vec<char> = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".chars().collect();
    let mut alpha_dic: HashMap<char, u32> = HashMap::new();

    // Initialize the alphabet frequencies to zero
    for &ch in &up_alphabet {
        alpha_dic.insert(ch, 0);
    }

    // Count the frequency of each letter and total number of alphabetic characters
    let mut num_alpha = 0;
    for ch in msg.chars() {
        if let Some(ch) = ch.to_uppercase().next() {
            if up_alphabet.contains(&ch) {
                *alpha_dic.entry(ch).or_insert(0) += 1;
                num_alpha += 1;
            }
        }
    }

    // Calculate the Index of Coincidence
    let mut ic: f64 = 0.0;
    if num_alpha > 1 {
        for &ch in &up_alphabet {
            let count = *alpha_dic.get(&ch).unwrap_or(&0) as f64;
            ic += count * (count - 1.0);
        }
        ic /= (num_alpha as f64) * (num_alpha as f64 - 1.0);
    }
    ic
}

fn main() {
    let msg1: &str = "What is Caesar cipher? Is it secure?";
    let msg2: &str = "Zkdw lv Fdhvdu flskhu? Lv lw vhfxuh?";

    println!("msg1 = {}, ...", &msg1[..30]);
    println!("msg2 = {}, ...", &msg2[..30]);
    println!("Index of Coincidence, IC(msg1) = {:.4}", ic(msg1));
    println!("Index of Coincidence, IC(msg2) = {:.4}", ic(msg2));
}