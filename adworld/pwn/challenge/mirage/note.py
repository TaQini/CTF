#!/usr/bin/python
#__author__:TaQini

from pwn import *

local_file  = './note'
local_libc  = '/lib/x86_64-linux-gnu/libc.so.6'
remote_libc = '../libc.so.6'

if len(sys.argv) == 1:
    p = process(local_file)
    libc = ELF(local_libc)
elif len(sys.argv) > 1:
    host, port = sys.argv[1].split(':')
    if len(sys.argv) == 3:
        host = sys.argv[1]
        port = sys.argv[2]
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
    gdb.attach(p,cmd)

# info
# gadget
prdi = 0x000000000040228b # add al, ch ; jmp rdi
0x0000000000402289 # add byte ptr [rax], al ; add al, ch ; jmp rdi
0x000000000040123b # add byte ptr [rbp + rax - 0x18], dh ; insd dword ptr [rdi], dx ; idiv edi ; dec ecx ; ret
0x0000000000401f50 # cmpsb byte ptr [rsi], byte ptr [rdi] ; nop ; pop rbp ; ret
0x000000000040123f # insd dword ptr [rdi], dx ; idiv edi ; dec ecx ; ret
0x000000000040228d # jmp rdi
0x0000000000402ca3 # pop rdi ; pop rbp ; ret
0x0000000000403ad3 # pop rdi ; ret

# elf, libc

# rop1
offset = 0
payload = 'A'*offset
payload += ''

# ru('')
# sl(payload)

# debug()
# info_addr('tag',addr)
# log.warning('--------------')

p.interactive()

