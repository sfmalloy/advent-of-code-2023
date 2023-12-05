    .intel_syntax noprefix
    .text
    .global _start

/***************************************************************************/
# NOTES

# Syscall numbers
# write    1
# open     2
# close    3
# fstat    5
# mmap     9
# munmap  11

# FUNCTION calling convention param order
# rdi, rsi, rdx, rcx, r8 and r9

# SYSCALL calling convention param order
# rdi, rsi, rdx, r10, r8 and r9

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
    push rbp
    mov rbp, rsp
    push rbx                        # expect
    push r12                        # actual
    push r13                        # expect_len
    push r14                        # index
    push r15                        # equal flag

    mov rbx, rdi
    mov r12, rsi
    mov r13, rdx
    xor r14, r14
    mov r15, 1
    xor r10, r10
    xor r11, r11
.str_equal_loop:
    cmp r14, r13
    je .str_equal_exit

    mov r10b, BYTE PTR [rbx+r14]
    mov r11b, BYTE PTR [r12+r14]
    cmp r10, r11
    jne .str_not_equal
    inc r14
    jmp .str_equal_loop
.str_not_equal:
    mov r15, 0
.str_equal_exit:
    mov rax, r15
    pop r15
    pop r14
    pop r13
    pop r12
    pop rbx
    leave
    ret

/****************************************************************************/
/**
    // in-place reverses a string
    void str_reverse(char* str, size_t length);
*/
str_reverse:
    push rbp
    mov rbp, rsp
    push rbx                        # str
    push r12                        # forward index
    push r13                        # backward index
    mov rbx, rdi
    xor r12, r12
    mov r13, rsi
.str_reverse_loop:
    cmp r12, r13
    je .str_reverse_copy_setup

    dec rsp
    mov r10b, BYTE PTR [rbx+r12]
    mov BYTE PTR [rsp], r10b
    inc r12
    jmp .str_reverse_loop
.str_reverse_copy_setup:
    xor r12, r12
.str_reverse_copy_loop:
    cmp r12, r13
    je .str_reverse_exit
    mov r10b, BYTE PTR [rsp+r12]
    mov BYTE PTR [rbx+r12], r10b
    inc r12
    jmp .str_reverse_copy_loop
.str_reverse_exit:
    add rsp, r13
    pop r13
    pop r12
    pop rbx
    leave
    ret

/****************************************************************************/
/**
    char* substr(char* str, size_t start, size_t len, char* buf)
*/
substr:
    push rbp
    mov rbp, rsp
    push rbx                        # str
    push r12                        # start
    push r13                        # len
    push r14                        # buf
    push r15                        # buf_idx
    mov rbx, rdi
    mov r12, rsi
    mov r13, rdx
    mov r14, rcx
    xor r15, r15
.substr_loop:
    cmp r15, r13
    je .substr_exit
    xor r10, r10
    mov r10b, BYTE PTR [rbx+r12]
    mov BYTE PTR [r14+r15], r10b
    inc r12
    inc r15
    jmp .substr_loop
.substr_exit:
    pop r15
    pop r14
    pop r13
    pop r12
    pop rbx
    leave
    ret

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
    char part2_first_digit(char* word, size_t len)
*/
part2_first_digit:
    push rbp
    mov rbp, rsp
    sub rsp, 32
    push rbx
    push r12
    push r13
    push r14
    push r15
    mov rbx, rdi
    xor r12, r12
    mov r13, rsi
.part2_first_digit_loop:
    cmp r12, r13
    je .part2_first_digit_exit
    
    mov dil, BYTE PTR [rbx+r12]
    call is_digit
    cmp eax, 1
    je .part2_first_digit_no_word_exit

    mov r14, 2
.part2_first_digit_substr_loop:
    inc r14
    cmp r14, 6
    jne .part2_first_digit_substr_loop_start
    inc r12
    jmp .part2_first_digit_loop
.part2_first_digit_substr_loop_start:
    mov rdi, rbx
    mov rsi, r12
    mov rdx, r14
    lea rcx, BYTE PTR [rbp-8]
    call substr

    xor r15, r15
    mov QWORD PTR [rbp-16], 0
    mov r10d, DWORD PTR [NUM_NAMES_LEN]
    mov QWORD PTR [rbp-24], r10
.part2_first_digit_name_loop:
    mov r10, QWORD PTR [rbp-16]
    lea rdi, [NUM_NAMES+r10]
    lea rsi, BYTE PTR [rbp-8]
    mov rdx, QWORD PTR [rbp-24]
    call str_equal

    inc r15
    cmp rax, 1
    jne .part2_first_digit_name_loop_inc
    mov rax, r15
    jmp .part2_first_digit_exit
.part2_first_digit_name_loop_inc:
    cmp r15, 9
    je .part2_first_digit_substr_loop

    mov r11, r15
    imul r11, 4
    mov r10, QWORD PTR [rbp-24]
    inc r10
    add QWORD PTR [rbp-16], r10
    mov r10d, DWORD PTR [NUM_NAMES_LEN+r11]
    mov QWORD PTR [rbp-24], r10
    jmp .part2_first_digit_name_loop
.part2_first_digit_no_word_exit:
    mov al, BYTE PTR [rbx+r12]
    sub al, 0x30
.part2_first_digit_exit:
    add al, 0x30
    pop r15
    pop r14
    pop r13
    pop r12
    pop rbx
    add rsp, 32
    leave
    ret

/****************************************************************************/
/**
    char part2_last_digit(char* word, size_t len)
*/
part2_last_digit:
    push rbp
    mov rbp, rsp
    sub rsp, 32
    push rbx                        # word
    push r12
    push r13                        # len
    push r14
    push r15
    mov rbx, rdi
    xor r12, r12
    mov r13, rsi

    mov rdi, rbx
    mov rsi, r13
    call str_reverse
.part2_last_digit_loop:
    cmp r12, r13
    je .part2_last_digit_exit
    
    mov dil, BYTE PTR [rbx+r12]
    call is_digit
    cmp eax, 1
    je .part2_last_digit_no_word_exit

    mov r14, 2
.part2_last_digit_substr_loop:
    inc r14
    cmp r14, 6
    jne .part2_last_digit_substr_loop_start
    inc r12
    jmp .part2_last_digit_loop
.part2_last_digit_substr_loop_start:
    mov rdi, rbx
    mov rsi, r12
    mov rdx, r14
    lea rcx, BYTE PTR [rbp-8]
    call substr

    xor r15, r15
    mov QWORD PTR [rbp-16], 0
    mov r10d, DWORD PTR [NUM_NAMES_LEN]
    mov QWORD PTR [rbp-24], r10
.part2_last_digit_name_loop:
    mov r10, QWORD PTR [rbp-16]
    lea rdi, [REVERSE_NUM_NAMES+r10]
    lea rsi, BYTE PTR [rbp-8]
    mov rdx, QWORD PTR [rbp-24]
    call str_equal

    inc r15
    cmp rax, 1
    jne .part2_last_digit_name_loop_inc
    mov rax, r15
    jmp .part2_last_digit_exit
.part2_last_digit_name_loop_inc:
    cmp r15, 9
    je .part2_last_digit_substr_loop

    mov r11, r15
    imul r11, 4
    mov r10, QWORD PTR [rbp-24]
    inc r10
    add QWORD PTR [rbp-16], r10
    mov r10d, DWORD PTR [NUM_NAMES_LEN+r11]
    mov QWORD PTR [rbp-24], r10
    jmp .part2_last_digit_name_loop
.part2_last_digit_no_word_exit:
    mov al, BYTE PTR [rbx+r12]
    sub al, 0x30
.part2_last_digit_exit:
    add al, 0x30
    push rax

    mov rdi, rbx
    mov rsi, r13
    call str_reverse

    pop rax
    pop r15
    pop r14
    pop r13
    pop r12
    pop rbx
    add rsp, 32
    leave
    ret
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
    xor rdx, 2                      # PROT_WRITE
    mov r10, 2                      # MAP_PRIVATE
    mov r8, rbx
    xor r9, r9
    mov rax, 9
    syscall
    mov r13, rax                    # input = mmap(NULL, fsize, PROT_READ, MAP_SHARED, fd, 0)

    sub rsp, 18
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

    lea rdi, [r13+r15]
    mov rsi, r14
    call part2_first_digit
    mov BYTE PTR [rbp-2], al

    lea rdi, [r13+r15]
    mov rsi, r14
    call part2_last_digit
    mov BYTE PTR [rbp-1], al

    lea rdi, [rbp-2]
    call str_to_int
    add QWORD PTR [rbp-18], rax

    add r15, r14
    inc r15
    jmp .main_loop
.cleanup:
    mov rdi, QWORD PTR [rbp-10]
    call write_int

    mov rdi, QWORD PTR [rbp-18]
    call write_int

    add rsp, 18

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
OTHER_TEST_STRING:
    .string "cool"
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
REVERSE_NUM_NAMES:
    .string "eno"
    .string "owt"
    .string "eerht"
    .string "ruof"
    .string "evif"
    .string "xis"
    .string "neves"
    .string "thgie"
    .string "enin"
    .align 8
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
