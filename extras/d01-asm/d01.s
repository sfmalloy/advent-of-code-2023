    .intel_syntax noprefix
    .text
    .global _start

# read    0
# write   1
# open    2
# close   3
# fstat   5
# mmap    9
# munmap 11

# FUNCTION calling convention param order
# %rdi, %rsi, %rdx, %rcx, %r8 and %r9

# SYSCALL calling convention param order
# %rdi, %rsi, %rdx, %r10, %r8 and %r9

/****************************************************************************/
/**
    bool is_digit(char c)
*/
is_digit:
    push rbp
    mov rbp, rsp

    xor eax, eax
    cmp dil, 0x30
    jl .is_digit_ret
    cmp dil, 0x39
    jg .is_digit_ret
    mov eax, 1
.is_digit_ret:
    leave
    ret

/****************************************************************************/
/**
    int line_len(char* line)
*/
line_len:
    push rbp
    mov rbp, rsp
    push rbx
    push r12
    mov rbx, rdi
    xor r12, r12
.line_len_loop:
    cmp BYTE PTR [rbx+r12], 0xa
    je .line_len_exit
    inc r12
    jmp .line_len_loop
.line_len_exit:
    mov rax, r12
    pop r12
    pop rbx
    leave
    ret

/****************************************************************************/
/**
    int str_to_int(char* str)
*/
str_to_int:
    push rbp
    mov rbp, rsp
    push rbx
    mov rbx, rdi
    
    mov al, BYTE PTR [rbx]
    sub al, 0x30
    imul rax, 10
    add al, BYTE PTR [rbx+1]
    sub al, 0x30

    pop rbx
    leave
    ret
/****************************************************************************/
/**
    bool str_equal(char* expect, char* actual, size_t expect_len)
*/
str_equal:

/****************************************************************************/
/**
    char part1_first_digit(char* word, size_t len)
*/
part1_first_digit:
    push rbp
    mov rbp, rsp
    push rbx
    push r12
    push r13
    mov rbx, rdi
    xor r12, r12
    mov r13, rsi
.part1_first_digit_loop:
    cmp r12, r13
    je .part1_first_digit_exit
    mov dil, BYTE PTR [rbx+r12]
    call is_digit
    cmp eax, 0
    je .part1_first_digit_inc
    mov al, BYTE PTR [rbx+r12]
    jmp .part1_first_digit_exit
.part1_first_digit_inc:
    inc r12
    jmp .part1_first_digit_loop
.part1_first_digit_exit:
    pop r13
    pop r12
    pop rbx
    leave
    ret

/****************************************************************************/
/**
    char part1_last_digit(char* word, size_t len)
*/
part1_last_digit:
    push rbp
    mov rbp, rsp
    push rbx
    push r12
    push r13
    mov rbx, rdi
    mov r12, rsi
    mov r13, r12
    dec r13
.part1_last_digit_loop:
    cmp r12, 0
    jl .part1_last_digit_exit
    mov dil, BYTE PTR [rbx+r12]
    call is_digit
    cmp eax, 0
    je .part1_last_digit_inc
    mov al, BYTE PTR [rbx+r12]
    jmp .part1_last_digit_exit
.part1_last_digit_inc:
    dec r12
    jmp .part1_last_digit_loop
.part1_last_digit_exit:
    pop r13
    pop r12
    pop rbx
    leave
    ret

/****************************************************************************/
/**
    int part1_test(char* word)
*/
part1_test:
    push rbp
    mov rbp, rsp
    push rbx
    push r12
    push r13
    mov rbx, rdi
    xor r12, r12
    xor r13, r13
.part1_loop:
    cmp BYTE PTR [rbx+r12], 0xa     # if (char == '\n) exit
    je .part1_exit
    mov dil, BYTE PTR [rbx+r12]
    call is_digit
    cmp eax, 0                      # if (!is_digit(char)) ...
    je .part1_inc
    inc r13
.part1_inc:
    inc r12                         # ++idx
    jmp .part1_loop
.part1_exit:
    mov rax, r13
    pop r13
    pop r12
    pop rbx
    leave
    ret
/****************************************************************************/
part2_first_digit:
/****************************************************************************/
part2_last_digit:
/****************************************************************************/
part2_test:


/****************************************************************************/
/**
    void write_int(int num)
*/
write_int:
    push rbp
    mov rbp, rsp
    push rbx
    push r12

    mov r12, 1
    dec rsp                         # rsp acts as string buffer
    mov BYTE PTR [rsp], 0xa         # append '\n'

    mov rbx, rdi
    mov rcx, 10
.write_int_loop:
    xor rdx, rdx
    mov rax, rbx
    idiv rcx
    mov rbx, rax                    # num /= 10
    add rdx, 0x30                   # char += '0'

    inc r12                         # len += 1
    dec rsp                         # increase string buffer size
    mov BYTE PTR [rsp], dl          # append digit (dl == 8-bit rdx)

    test rbx, rbx                   # if (rbx == 0) exit loop
    je .write_int_exit
    jmp .write_int_loop
.write_int_exit:
    mov rdi, 1
    lea rsi, QWORD PTR [rsp]
    mov rdx, r12
    mov rax, 1
    syscall

    add rsp, r12
    pop r12
    pop rbx
    leave
    ret

/****************************************************************************/

_start:
    mov rbp, rsp
    push rbx                        # fd
    push r12                        # fsize
    push r13                        # input
    push r14                        # line_len
    push r15                        # input_idx

                                    # accessing a string from NUM_NAMES
                                    # mov r11d, DWORD PTR [NUM_NAMES_LEN+4]
                                    # inc r11
                                    # lea rdi, NUM_NAMES
                                    # add rdi, r11
    lea rdi, FILENAME
    mov rsi, 0
    mov rax, 2
    syscall
    mov rbx, rax                    # rbx = open("d01.in", O_RDONLY)

    sub rsp, 144                    # allocate memory for stat structure
    mov rdi, rbx
    lea rsi, [rbp-144]
    mov rax, 5
    syscall                         # struct stat file_stat = fstat(rbx, &(rbp-144))
    mov r12, QWORD PTR [rbp-96]     # fsize = file_stat.st_size
    add rsp, 144                    # unallocate fstat memory

    xor rdi, rdi
    mov rsi, r12
    mov rdx, 1                      # PROT_READ
    mov r10, 2                      # MAP_PRIVATE
    mov r8, rbx
    xor r9, r9
    mov rax, 9
    syscall
    mov r13, rax                    # input = mmap(NULL, fsize, PROT_READ, MAP_SHARED, fd, 0)

    sub rsp, 10
    xor r15, r15
    mov QWORD PTR [rbp-10], 0
.main_loop:
    cmp r15, r12
    jge .cleanup

    lea rdi, [r13+r15]
    call line_len
    mov r14, rax

    lea rdi, [r13+r15]
    mov rsi, r14
    call part1_first_digit
    mov BYTE PTR [rbp-2], al

    lea rdi, [r13+r15]
    mov rsi, r14
    call part1_last_digit
    mov BYTE PTR [rbp-1], al

    lea rdi, [rbp-2]
    call str_to_int
    add QWORD PTR [rbp-10], rax

    add r15, r14
    inc r15
    jmp .main_loop

.cleanup:
    mov rdi, QWORD PTR [rbp-10]
    call write_int

    add rsp, 10

    mov rdi, r13
    mov rsi, r12
    mov rax, 11
    syscall                         # munmap(input)

    mov rdi, rbx
    mov rax, 3
    syscall                         # close(fd)

    pop r15
    pop r14
    pop r13
    pop r12
    pop rbx
    xor rdi, rdi
    mov rax, 60                     # exit(0)
    syscall

/****************************************************************************/

    .data
    .align 8
FILENAME:
    .string "d01.in"
NUM_NAMES:
    .string "one"
    .string "two"
    .string "three"
    .string "four"
    .string "five"
    .string "six"
    .string "seven"
    .string "eight"
    .string "nine"
NUM_NAMES_LEN:
    .long 3
    .long 3
    .long 5
    .long 4
    .long 4
    .long 3
    .long 5
    .long 5
    .long 4
