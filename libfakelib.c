//
// Created by fxman on 2021/1/13.
//

#include "library.h"

pid_t fork(void) {
    exit(1);
}

int execv(const char *pathname, char * const argv[]) {
    exit(1);
}

int clone(int (*fn)(void *), void *child_stack, int flags, void *arg) {
    exit(1);
}

int kill(pid_t pid,int signo) {
    exit(1);
}

pid_t vfork(void) {
    exit(1);
}
