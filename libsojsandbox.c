#include "library.h"

int
sandbox_exec(char *exec_file_location, char *sample_location, char *output_location, int time_limit, int memory_limit) {
    char prefix[128] = "LD_PRELOAD=./libfakelib.so ";
    struct rlimit cpu_limit;
    struct rlimit vm_limit;

    strcat(prefix, exec_file_location);

    cpu_limit.rlim_cur = time_limit * 3 / 1000;
    cpu_limit.rlim_max = time_limit * 3 / 1000;

    vm_limit.rlim_cur = memory_limit * 3 * 1024 * 1024;
    vm_limit.rlim_max = memory_limit * 3 * 1024 * 1024;

    freopen(sample_location, "r", stdin);
    freopen(output_location, "w", stdout);

    setrlimit(RLIMIT_AS, &vm_limit);
    setrlimit(RLIMIT_CPU, &cpu_limit);

    system(prefix);

    exit(0);
}
