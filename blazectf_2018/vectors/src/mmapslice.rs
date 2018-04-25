use libc::{O_CREAT, O_RDWR, O_TRUNC};
use libc::{PROT_READ, PROT_WRITE, MAP_FAILED, MAP_SHARED};
use libc::{close, mmap, munmap, open, posix_fallocate};
use std::ffi::CString;
use std::{mem, ptr, slice};

pub struct MMapSlice<'a, T: 'a> { fd: i32, pub data: &'a mut [T] }

impl<'a, T: 'a> MMapSlice<'a, T> {
    /// This unsafe for the same reasons as mem::zeroed, and the ptr::write 
    ///  workaround from mem::uninitialized's documentation should be used to 
    ///  initialize the memory for any types with non-trivial Drop impls
    pub unsafe fn new<P: Into<Vec<u8>>>(p: P, len: usize, create: bool) -> Option<MMapSlice<'a, T>> {
        let path = if let Ok(s) = CString::new(p.into()) { s } else { return None };
        let bytelen = len * mem::size_of::<T>();
        let (flags, mode) = if create { (O_CREAT | O_TRUNC, 0o600) } else { (0, 0) };
        let fd = open(path.as_ptr(), O_RDWR | flags, mode);
        if fd == -1 { return None };
        if posix_fallocate(fd, 0, bytelen as _) != 0 { return None };
        let ptr : *mut T = mmap(ptr::null_mut(), bytelen, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0) as _;
        if ptr == MAP_FAILED as _ { return None; }
        Some(MMapSlice { fd, data: slice::from_raw_parts_mut(ptr, len) })
    }
}

impl<'a, T> Drop for MMapSlice<'a, T> {
    fn drop(&mut self) {
        let (ptr, len) = (self.data.as_mut_ptr(), self.data.len());
        let bytelen = len * mem::size_of::<T>();
        unsafe {
            // both munmap and close can fail, but drop's signature admits no non-panic way to signal failure
            if munmap(ptr as _, bytelen) == -1 { panic!("munmap failed in MMapSlice::drop") };
            if close(self.fd) == -1 { panic!("close failed in MMapSlice::drop") };
        }
    }
}

#[test]
fn test1() {
    let len = 32;
    let a: MMapSlice<u32> = unsafe { MMapSlice::new(b"test1.mmap".as_ref(), len, true).unwrap() };
    for x in a.data.iter_mut() {
        assert_eq!(*x, 0);
        *x = 0x41424344;
    }
    drop(a);
    let b: MMapSlice<u64> = unsafe { MMapSlice::new(b"test1.mmap".as_ref(), len/2, false).unwrap() };
    for x in b.data.iter() {
        assert_eq!(*x, 0x4142434441424344);
    }
    drop(b);
}

