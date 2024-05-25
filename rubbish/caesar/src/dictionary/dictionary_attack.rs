use std::collections::HashMap;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

const LETTERS: &str = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz \t\n";

pub fn load_dic() -> io::Result<HashMap<String, usize>> {
    let mut english_dic = HashMap::new();
    let path = Path::new("EngDic.txt");
    let file = File::open(&path)?;
    let lines = io::BufReader::new(file).lines();

    for line in lines {
        if let Ok(word) = line {
            english_dic.insert(word.clone(), word.len());
        }
    }

    Ok(english_dic)
}

fn remove_non_letters(message: &str) -> String {
    message.chars()
           .filter(|c| LETTERS.contains(*c))
           .collect()
}

fn percent_english_words(message: &str, english_dic: &HashMap<String, usize>) -> f64 {
    let words: Vec<&str> = message.to_lowercase()
                                  .split_whitespace()
                                  .collect();
    if words.is_empty() {
        return 0.0;
    }
    let count_words = words.iter()
                           .filter(|&&word| english_dic.contains_key(word))
                           .count();

    count_words as f64 / words.len() as f64
}

fn is_english(message: &str, english_dic: &HashMap<String, usize>, word_percentage: f64, letter_percentage: f64) -> bool {
    let num_letters = remove_non_letters(message).len();
    let message_letters_percentage = num_letters as f64 / message.len() as f64 * 100.0;
    let letters_match = message_letters_percentage >= letter_percentage;

    let word_match = percent_english_words(message, english_dic) * 100.0 >= word_percentage;

    letters_match && word_match
}