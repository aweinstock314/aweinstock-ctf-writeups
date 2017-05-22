extern crate byteorder;
extern crate openssl_sys;
extern crate rayon;

use rayon::prelude::*;
use byteorder::ByteOrder;
use byteorder::LittleEndian;
use openssl_sys::*;
use std::ptr;
use std::time::Instant;
use std::sync::atomic::{AtomicUsize, Ordering};

fn main() {
/*
>>> [__import__('urllib').unquote(x).decode('base64').encode('hex') for x in ['W2YjSb0T5AyTbYSOl5%2F7Yw%3D%3D', '62nxynGM2XacQn4LmerEjQ%3D%3D', '0y3AnzWnob5HhBEz3Teiyg%3D%3D', 'itcmCH7HcVR6BHz%2FnISjUg%3D%3D']]
['5b662349bd13e40c936d848e979ffb63', 'eb69f1ca718cd9769c427e0b99eac48d', 'd32dc09f35a7a1be47841133dd37a2ca', '8ad726087ec771547a047cff9c84a352']
*/
    let ctxts = [
        [0x5b, 0x66, 0x23, 0x49, 0xbd, 0x13, 0xe4, 0x0c, 0x93, 0x6d, 0x84, 0x8e, 0x97, 0x9f, 0xfb, 0x63],
        [0xeb, 0x69, 0xf1, 0xca, 0x71, 0x8c, 0xd9, 0x76, 0x9c, 0x42, 0x7e, 0x0b, 0x99, 0xea, 0xc4, 0x8d],
        [0xd3, 0x2d, 0xc0, 0x9f, 0x35, 0xa7, 0xa1, 0xbe, 0x47, 0x84, 0x11, 0x33, 0xdd, 0x37, 0xa2, 0xca],
        [0x8a, 0xd7, 0x26, 0x08, 0x7e, 0xc7, 0x71, 0x54, 0x7a, 0x04, 0x7c, 0xff, 0x9c, 0x84, 0xa3, 0x52]
    ];
    let ctxts = [*b"\xdb\x92\x05\x2d\xe5\xa1\xed\x23\x48\x44\x83\x98\x55\xab\x85\x9c",
                 *b"\xba\x76\x7c\xa3\x9e\x87\xa7\x39\x2d\xbc\x72\x22\x9a\x6a\x71\x49",
                 *b"\xd5\xa6\x49\x32\xed\xc3\x33\x45\x50\xcb\x4b\x4c\x94\x48\x73\xc3",
                 *b"\x46\x58\xd4\x47\x9f\x4e\x8d\xbc\x7d\x95\x33\xc5\x8f\x42\x38\xfd"];
/*
<li><a href='?raofc=W2YjSb0T5AyTbYSOl5%2F7Yw%3D%3D'> RaoFC about Key Entropy Requirements </a></li>
<li><a href='?raofc=62nxynGM2XacQn4LmerEjQ%3D%3D'> RaoFC about Key Management Requirements </a></li>
<li><a href='?raofc=0y3AnzWnob5HhBEz3Teiyg%3D%3D'> RaoFc on RaoFc </a></li>
<li><a href='?raofc=itcmCH7HcVR6BHz%2FnISjUg%3D%3D'> RaoFC on Hashing Requirements </a></li>
---
>>> [__import__('urllib').unquote(x).decode('base64').encode('hex') for x in ['W2YjSb0T5AyTbYSOl5%2F7Yw%3D%3D', '62nxynGM2XacQn4LmerEjQ%3D%3D', '0y3AnzWnob5HhBEz3Teiyg%3D%3D', 'itcmCH7HcVR6BHz%2FnISjUg%3D%3D']]
['5b662349bd13e40c936d848e979ffb63', 'eb69f1ca718cd9769c427e0b99eac48d', 'd32dc09f35a7a1be47841133dd37a2ca', '8ad726087ec771547a047cff9c84a352']
---
:s/'/"/g
:'<,'>s/"/ *b"
:'<,'>s/[0-9a-f]\{2\}/\\x\0/g
*/
    let ctxts = [*b"\x5b\x66\x23\x49\xbd\x13\xe4\x0c\x93\x6d\x84\x8e\x97\x9f\xfb\x63",
                 *b"\xeb\x69\xf1\xca\x71\x8c\xd9\x76\x9c\x42\x7e\x0b\x99\xea\xc4\x8d",
                 *b"\xd3\x2d\xc0\x9f\x35\xa7\xa1\xbe\x47\x84\x11\x33\xdd\x37\xa2\xca",
                 *b"\x8a\xd7\x26\x08\x7e\xc7\x71\x54\x7a\x04\x7c\xff\x9c\x84\xa3\x52"];
/*
<li><a href='?raofc=amcXnAkkZ9VJStb8zXQIoQ%3D%3D'> RaoFC about Key Entropy Requirements </a></li>
<li><a href='?raofc=GGZ9T%2FwiDq7cNU2vkmoLPg%3D%3D'> RaoFC about Key Management Requirements </a></li>
<li><a href='?raofc=f5IgisSDZ6DbIyHm4vn%2Fpw%3D%3D'> RaoFc on RaoFc </a></li>
<li><a href='?raofc=7FrgDb9KLzwseSAyXg6g2A%3D%3D'> RaoFC on Hashing Requirements </a></li>
---
>>> [__import__('urllib').unquote(x).decode('base64').encode('hex') for x in ['amcXnAkkZ9VJStb8zXQIoQ%3D%3D', 'GGZ9T%2FwiDq7cNU2vkmoLPg%3D%3D', 'f5IgisSDZ6DbIyHm4vn%2Fpw%3D%3D', '7FrgDb9KLzwseSAyXg6g2A%3D%3D']]
['6a67179c092467d5494ad6fccd7408a1', '18667d4ffc220eaedc354daf926a0b3e', '7f92208ac48367a0db2321e6e2f9ffa7', 'ec5ae00dbf4a2f3c2c7920325e0ea0d8']
*/
    let ctxts = [*b"\x6a\x67\x17\x9c\x09\x24\x67\xd5\x49\x4a\xd6\xfc\xcd\x74\x08\xa1", *b"\x18\x66\x7d\x4f\xfc\x22\x0e\xae\xdc\x35\x4d\xaf\x92\x6a\x0b\x3e", *b"\x7f\x92\x20\x8a\xc4\x83\x67\xa0\xdb\x23\x21\xe6\xe2\xf9\xff\xa7", *b"\xec\x5a\xe0\x0d\xbf\x4a\x2f\x3c\x2c\x79\x20\x32\x5e\x0e\xa0\xd8"];

    openssl_sys::init();
    let trials = AtomicUsize::new(0);
    let end: u32 = 0u32.wrapping_sub(1);
    let starttime = Instant::now();
    let loopbody = |i| {
        let numtrials = trials.fetch_add(1, Ordering::Relaxed);
        if numtrials.count_ones() == 1 {
            println!("{}/{} approx {}, elapsed: {:?}", numtrials, end, (numtrials as f64 / end as f64), starttime.elapsed());
        }
        let mut found = true;
        for &ctxt in ctxts.iter() {
            let ptxt = crypt(i, Mode::Decrypt, ctxt);
            // We know the plaintexts have at least one pipe
            if let None = ptxt.iter().find(|&&x| x == b'|') { found = false; }
            // We assume that the plaintext is less than a full block, and padded standardly
            if !is_valid_padding(ptxt) { found = false; }
            // We assume that most of the bytes will be printable?
            //if !(ptxt.iter().filter(|&&x| 0x20 <= x && x < 0x7f).count() > 9) { found = false; }
        }
        if found {
            print!("found: {}; [''.join(map(chr,x)) for x in [", i);
            for &ctxt in ctxts.iter() {
                let ptxt = crypt(i, Mode::Decrypt, ctxt);
                print!("{:?},", ptxt);
            }
            println!("]]");
        }
    };
    /*for i in 0..end {
        //println!("i: {}", i);
        loopbody(i);
    }*/
    (0..end).into_par_iter().for_each(loopbody);
    //loopbody(end); // ranges are exclusive
}

const BLOCKSIZE: usize = 16;
enum Mode { Encrypt, Decrypt }
fn crypt(key: u32, mode: Mode, input: [u8; BLOCKSIZE]) -> [u8; BLOCKSIZE] {
    let mut key_bytes = [0;32];
    LittleEndian::write_u32(&mut key_bytes[0..4], key);

    let mut output = [0; BLOCKSIZE];
    thread_local!(static CTX: *mut EVP_CIPHER_CTX = unsafe { EVP_CIPHER_CTX_new() });
    thread_local!(static ECB: *const EVP_CIPHER = unsafe { EVP_aes_256_ecb() });
    CTX.with(|&ctx| { ECB.with(|&ecb| {
        let mode = match mode { Mode::Encrypt => 1, Mode::Decrypt => 0 };
        unsafe { EVP_CipherInit_ex(ctx, ecb, ptr::null_mut(), key_bytes.as_ptr(), ptr::null(), mode) };
        let mut len = 0;
        unsafe { EVP_CipherUpdate(ctx, output.as_mut_ptr(), &mut len, input.as_ptr(), input.len() as i32) };
        //assert_eq!(len as usize, BLOCKSIZE); // This assert fails on decryption, but it seems to be getting the right answer for decryption (as witnessed by test_aes_php_compat)
        //unsafe { EVP_CIPHER_CTX_free(ctx) };
    })});
    output
}

#[test]
fn test_aes_php_compat() {
/*
$ php -a
php > echo openssl_encrypt("0123456789ABCDEF", "AES-256-ECB", "AAAA");
zaluKTXN5sjkmStmfRxRlQ2NGNT8qwure4VxX1UzD3M=
---
$ python
>>> import Crypto.Cipher.AES
>>> Crypto.Cipher.AES.new('AAAA'+'\x00'*28).encrypt("0123456789ABCDEF").encode('base64')
'zaluKTXN5sjkmStmfRxRlQ==\n'
>>> Crypto.Cipher.AES.new('AAAA'+'\x00'*28).decrypt('zaluKTXN5sjkmStmfRxRlQ2NGNT8qwure4VxX1UzD3M='.decode('base64'))
'0123456789ABCDEF\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10'
>>> list(map(ord,'zaluKTXN5sjkmStmfRxRlQ==\n'.decode('base64')))
[205, 169, 110, 41, 53, 205, 230, 200, 228, 153, 43, 102, 125, 28, 81, 149]
*/
    let ptxt = *b"0123456789ABCDEF";
    let ctxt = [205, 169, 110, 41, 53, 205, 230, 200, 228, 153, 43, 102, 125, 28, 81, 149];
    assert_eq!(crypt(0x41414141, Mode::Encrypt, ptxt), ctxt);
    assert_eq!(crypt(0x41414141, Mode::Decrypt, ctxt), ptxt);
}

#[test]
fn test_aes_php_compat2() {
/*
<li><a href='?raofc=25IFLeWh7SNIRIOYVauFnA%3D%3D'> RaoFC about Key Entropy Requirements </a></li>
<li><a href='?raofc=unZ8o56HpzktvHIimmpxSQ%3D%3D'> RaoFC about Key Management Requirements </a></li>
<li><a href='?raofc=1aZJMu3DM0VQy0tMlEhzww%3D%3D'> RaoFc on RaoFc </a></li>
<li><a href='?raofc=RljUR59Ojbx9lTPFj0I4%2FQ%3D%3D'> RaoFC on Hashing Requirements </a></li>
---
>>> [__import__('urllib').unquote(x).decode('base64').encode('hex') for x in ['25IFLeWh7SNIRIOYVauFnA%3D%3D', 'unZ8o56HpzktvHIimmpxSQ%3D%3D', '1aZJMu3DM0VQy0tMlEhzww%3D%3D', 'RljUR59Ojbx9lTPFj0I4%2FQ%3D%3D']]
['db92052de5a1ed234844839855ab859c', 'ba767ca39e87a7392dbc72229a6a7149', 'd5a64932edc3334550cb4b4c944873c3', '4658d4479f4e8dbc7d9533c58f4238fd']
*/
    let ctxts = [*b"\xdb\x92\x05\x2d\xe5\xa1\xed\x23\x48\x44\x83\x98\x55\xab\x85\x9c",
                 *b"\xba\x76\x7c\xa3\x9e\x87\xa7\x39\x2d\xbc\x72\x22\x9a\x6a\x71\x49",
                 *b"\xd5\xa6\x49\x32\xed\xc3\x33\x45\x50\xcb\x4b\x4c\x94\x48\x73\xc3",
                 *b"\x46\x58\xd4\x47\x9f\x4e\x8d\xbc\x7d\x95\x33\xc5\x8f\x42\x38\xfd"];
    let ptxts = [*b"A|0\x0d\x0d\x0d\x0d\x0d\x0d\x0d\x0d\x0d\x0d\x0d\x0d\x0d", 
                 *b"B|1\x0d\x0d\x0d\x0d\x0d\x0d\x0d\x0d\x0d\x0d\x0d\x0d\x0d",
                 *b"C|2\x0d\x0d\x0d\x0d\x0d\x0d\x0d\x0d\x0d\x0d\x0d\x0d\x0d",
                 *b"D|Admin\x09\x09\x09\x09\x09\x09\x09\x09\x09"];
    for (&ptxt, &ctxt) in ptxts.iter().zip(ctxts.iter()) {
        assert!(is_valid_padding(ptxt));
        assert_eq!(crypt(0x42424242, Mode::Encrypt, ptxt), ctxt);
        assert_eq!(crypt(0x42424242, Mode::Decrypt, ctxt), ptxt);
    }

}

fn is_valid_padding(ptxt: [u8; BLOCKSIZE]) -> bool {
    let count = ptxt[15] as usize;
    if count > BLOCKSIZE { return false; }
    if !(ptxt[BLOCKSIZE-count..].iter().all(|&x| x as usize == count)) { return false; }
    true
}

#[test]
fn test_valid_padding() {
    assert!(is_valid_padding(*b"\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10"));
    assert!(is_valid_padding(*b"0123456789ABCDE\x01"));
    assert!(is_valid_padding(*b"0123456789ABCD\x02\x02"));
    assert!(is_valid_padding(*b"0123456789ABC\x03\x03\x03"));
    assert!(!is_valid_padding(*b"0123456789ABCD\x02\x03"));
    assert!(!is_valid_padding(*b"0123456789ABCDE\x11"));
    assert!(!is_valid_padding(*b"0123456789ABCDEF"));
}
