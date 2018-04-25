#![feature(alloc_system)]
extern crate alloc_system;
extern crate smallvec;
extern crate libc;

mod mmapslice;
use mmapslice::*;

use libc::{STDIN_FILENO, rand, read, srand, time};
use smallvec::SmallVec;
use std::{io, mem, ptr};
use io::{BufRead, Write};

fn prompt_num(prompt: &str) -> Option<usize> {
    print!("{} ", prompt);
    io::stdout().flush().unwrap();
    let mut buf = String::new();
    io::stdin().read_line(&mut buf).ok()?;
    buf.pop(); //newline
    Some(buf.parse().ok()?)
}

fn main() {
    unsafe { srand(time(ptr::null_mut()) as _) };
    let slice: MMapSlice<SmallVec<[usize; 32]>> = unsafe { MMapSlice::new(format!("/tmp/map{}", rand()), 10, true) }.unwrap();
    let i = io::stdin();
    let mut o = io::stdout();
    loop {
        let mut buf = String::new();
        print!("read/write/push/pop> ");
        o.flush().unwrap();
        i.read_line(&mut buf).unwrap();
        match () {
            _ if buf.starts_with("read") => {
                if let Some(idx) = prompt_num("Which vec?") {
                    if let Some(vec) = slice.data.get(idx) {
                        if let Some(jdx) = prompt_num("index>") {
                            if let Some(x) = vec.get(jdx) {
                                println!("vec[{}][{}] == {}", idx, jdx, x);
                            } else {
                                println!("Sorry, vec[{}] only has {} elements", idx, vec.len());
                            }
                        }
                    }
                }
            },
            _ if buf.starts_with("write") => {
                if let Some(idx) = prompt_num("Which vec?") {
                    if let Some(vec) = slice.data.get_mut(idx) {
                        let len = vec.len();
                        if let Some(jdx) = prompt_num("index>") {
                            if let Some(x) = vec.get_mut(jdx) {
                                if let Some(y) = prompt_num("New value?") {
                                    *x = y;
                                }
                            } else {
                                println!("Sorry, vec[{}] only has {} elements", idx, len);
                            }
                        }
                    }
                }
            },
            _ if buf.starts_with("push") => {
                if let Some(idx) = prompt_num("Which vec?") {
                    if let Some(vec) = slice.data.get_mut(idx) {
                        if let Some(y) = prompt_num("New value?") {
                            vec.push(y);
                        }
                    }
                }
            },
            _ if buf.starts_with("pop") => {
                if let Some(idx) = prompt_num("Which vec?") {
                    if let Some(vec) = slice.data.get_mut(idx) {
                        if let Some(x) = vec.pop() {
                            println!("popped value was {}", x);
                        }
                        vec.shrink_to_fit();
                    }
                }
            },
            _ => return,
        }
        for vec in slice.data.iter() {
            // DEBUG:
            println!("{:?}, {}, {}", vec.as_ptr(), vec.len(), vec.capacity());
        }
    }
}
