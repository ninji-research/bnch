#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

typedef int64_t (*sarif_effect_handler_t)(uint64_t* args, int32_t nargs);
struct SarifEffectHandler {
    const char* effect;
    const char* operation;
    sarif_effect_handler_t handler;
};

extern void* sarif_record_alloc(uint64_t size);
extern void* sarif_text_concat(const unsigned char* left, const unsigned char* right);
extern uint64_t sarif_text_len(const unsigned char* text);
extern int64_t sarif_text_cmp(const unsigned char* left, const unsigned char* right);
extern uint64_t sarif_text_eq(const unsigned char* left, const unsigned char* right);
extern void* sarif_text_slice(const unsigned char* text, uint64_t start, uint64_t end);
extern void* sarif_bytes_slice(const unsigned char* bytes, uint64_t start, uint64_t end);
extern uint64_t sarif_bytes_len(const unsigned char* bytes);
extern int64_t sarif_bytes_byte(const unsigned char* bytes, uint64_t index);
extern void* sarif_bytes_materialize(const unsigned char* bytes);
extern int64_t sarif_parse_i32(const unsigned char* text);
extern void* sarif_text_from_f64_fixed(double value, int64_t digits);
extern void sarif_stdout_write(const unsigned char* text);
extern int64_t sarif_perform_effect(
    const char* effect, const char* operation,
    uint64_t arg0, uint64_t arg1, uint64_t arg2, uint64_t arg3,
    int32_t nargs);
extern uint64_t sarif_arg_count(void);
extern void* sarif_arg_text(int64_t index);
extern void* sarif_stdin_text(void);
extern void* sarif_list_new(int64_t len, uint64_t fill);
extern void* sarif_list_push(void* list, int64_t len, uint64_t value);
extern uint64_t sarif_list_get(void* list, int64_t index);
extern void* sarif_list_set(void* list, int64_t index, uint64_t value);
extern int64_t sarif_list_len(void* list);
extern uint64_t sarif_text_eq_range(const unsigned char* source, int64_t start, int64_t end, const unsigned char* expected);
extern int64_t sarif_text_find_byte_range(const unsigned char* source, int64_t start, int64_t end, int64_t byte);
extern int64_t sarif_text_line_end(const unsigned char* source, int64_t start);
extern int64_t sarif_text_next_line(const unsigned char* source, int64_t start);
extern int64_t sarif_text_next_field(const unsigned char* source, int64_t start, int64_t end, int64_t byte);
extern uint64_t sarif_file_open(const unsigned char* path, const unsigned char* mode);
extern void sarif_file_close(uint64_t handle);
extern void sarif_file_sync(uint64_t handle);
extern uint64_t sarif_file_read(uint64_t handle, int64_t len);
extern uint64_t sarif_file_read_to_end(uint64_t handle);
extern int64_t sarif_file_write(uint64_t handle, const unsigned char* data);
extern int64_t sarif_file_seek(uint64_t handle, int64_t offset, int64_t whence);
extern int64_t sarif_file_size(uint64_t handle);
extern int64_t sarif_file_exists(const unsigned char* path);
extern int64_t sarif_file_remove(const unsigned char* path);
extern int64_t sarif_file_is_valid(uint64_t handle);
extern uint64_t sarif_file_mmap(const unsigned char* path);
extern void* sarif_bytes_to_text(const unsigned char* bytes);
extern void* sarif_list_sort_text(void* list, int64_t len);
extern void* sarif_list_sort_by_text_field(void* list, int64_t len, int64_t offset);
extern void* sarif_text_builder_new(void);
extern void* sarif_text_builder_append(void* builder, const unsigned char* text);
extern void* sarif_text_builder_append_codepoint(void* builder, int64_t codepoint);
extern void* sarif_text_builder_append_ascii(void* builder, int64_t byte);
extern void* sarif_text_builder_append_slice(void* builder, const unsigned char* text, int64_t start, int64_t end);
extern void* sarif_text_builder_append_i32(void* builder, int64_t value);
extern void* sarif_text_builder_finish(void* builder);
extern void* sarif_stdout_write_builder(void* builder);
extern void* sarif_text_index_new(void);
extern void* sarif_text_intern(const unsigned char* text);
extern void* sarif_text_index_set(void* index, uint64_t key, int64_t value);
extern int64_t sarif_text_index_get(void* index, uint64_t key);
extern int64_t sarif_text_index_contains(void* index, uint64_t key);
extern int64_t sarif_text_index_get_or_insert(void* index, uint64_t key, int64_t next);
extern void* sarif_text_index_keys(void* index);
extern double sarif_parse_f64(const unsigned char* text);
extern int64_t sarif_parse_i32_range(const unsigned char* text, int64_t start, int64_t end);
extern void sarif_alloc_push(void);
extern void sarif_alloc_pop(void);
extern double sarif_f64_from_i32(int64_t value);

static inline __attribute__((unused)) uint64_t sarif_load_u64(const unsigned char* base, uint64_t offset) {
    uint64_t value;
    memcpy(&value, base + offset, sizeof(uint64_t));
    return value;
}
static inline __attribute__((unused)) void sarif_store_u64(unsigned char* base, uint64_t offset, uint64_t value) {
    memcpy(base + offset, &value, sizeof(uint64_t));
}
static inline __attribute__((unused)) double sarif_load_f64(const unsigned char* base, uint64_t offset) {
    double value;
    memcpy(&value, base + offset, sizeof(double));
    return value;
}
static inline __attribute__((unused)) void sarif_store_f64(unsigned char* base, uint64_t offset, double value) {
    memcpy(base + offset, &value, sizeof(double));
}


uint64_t next_seed(uint64_t p0);

uint64_t pick_iub_codepoint(uint64_t p0);

uint64_t pick_homo_codepoint(uint64_t p0);

void write_repeat_section(uint64_t p0, uint64_t p1, uint64_t p2);

uint64_t write_random_section(uint64_t p0, uint64_t p1, uint64_t p2, uint64_t p3);

uint64_t next_seed(uint64_t p0) {
    uint64_t __attribute__((unused)) v0;
    uint64_t __attribute__((unused)) v1;
    uint64_t __attribute__((unused)) v2;
    uint64_t __attribute__((unused)) v3;
    uint64_t __attribute__((unused)) v4;
    uint64_t __attribute__((unused)) v5;
    uint64_t __attribute__((unused)) v6;
    uint64_t __attribute__((unused)) v7;
    uint64_t __attribute__((unused)) v8;
    uint64_t __attribute__((unused)) v9;
    v0 = p0;
    v1 = 3877llu;
    v2 = v0 * v1;
    v3 = 29573llu;
    v4 = v2 + v3;
    v5 = 139968llu;
    v6 = (int64_t)v4 / (int64_t)v5;
    v7 = 139968llu;
    v8 = v6 * v7;
    v9 = v4 - v8;
    return v9;
}

uint64_t pick_iub_codepoint(uint64_t p0) {
    uint64_t __attribute__((unused)) v0;
    uint64_t __attribute__((unused)) v1;
    uint64_t __attribute__((unused)) v2;
    uint64_t __attribute__((unused)) v3;
    uint64_t __attribute__((unused)) v4;
    uint64_t __attribute__((unused)) v5;
    uint64_t __attribute__((unused)) v6;
    uint64_t __attribute__((unused)) v7;
    uint64_t __attribute__((unused)) v8;
    uint64_t __attribute__((unused)) v9;
    uint64_t __attribute__((unused)) v10;
    uint64_t __attribute__((unused)) v11;
    uint64_t __attribute__((unused)) v12;
    uint64_t __attribute__((unused)) v13;
    uint64_t __attribute__((unused)) v14;
    uint64_t __attribute__((unused)) v15;
    uint64_t __attribute__((unused)) v16;
    uint64_t __attribute__((unused)) v17;
    uint64_t __attribute__((unused)) v18;
    uint64_t __attribute__((unused)) v19;
    uint64_t __attribute__((unused)) v20;
    uint64_t __attribute__((unused)) v21;
    uint64_t __attribute__((unused)) v22;
    uint64_t __attribute__((unused)) v23;
    uint64_t __attribute__((unused)) v24;
    uint64_t __attribute__((unused)) v25;
    uint64_t __attribute__((unused)) v26;
    uint64_t __attribute__((unused)) v27;
    uint64_t __attribute__((unused)) v28;
    uint64_t __attribute__((unused)) v29;
    uint64_t __attribute__((unused)) v30;
    uint64_t __attribute__((unused)) v31;
    uint64_t __attribute__((unused)) v32;
    uint64_t __attribute__((unused)) v33;
    uint64_t __attribute__((unused)) v34;
    uint64_t __attribute__((unused)) v35;
    uint64_t __attribute__((unused)) v36;
    uint64_t __attribute__((unused)) v37;
    uint64_t __attribute__((unused)) v38;
    uint64_t __attribute__((unused)) v39;
    uint64_t __attribute__((unused)) v40;
    uint64_t __attribute__((unused)) v41;
    uint64_t __attribute__((unused)) v42;
    uint64_t __attribute__((unused)) v43;
    uint64_t __attribute__((unused)) v44;
    uint64_t __attribute__((unused)) v45;
    uint64_t __attribute__((unused)) v46;
    uint64_t __attribute__((unused)) v47;
    uint64_t __attribute__((unused)) v48;
    uint64_t __attribute__((unused)) v49;
    uint64_t __attribute__((unused)) v50;
    uint64_t __attribute__((unused)) v51;
    uint64_t __attribute__((unused)) v52;
    uint64_t __attribute__((unused)) v53;
    uint64_t __attribute__((unused)) v54;
    uint64_t __attribute__((unused)) v55;
    uint64_t __attribute__((unused)) v56;
    uint64_t __attribute__((unused)) v57;
    uint64_t __attribute__((unused)) v58;
    uint64_t __attribute__((unused)) v59;
    uint64_t __attribute__((unused)) v60;
    uint64_t __attribute__((unused)) v61;
    uint64_t __attribute__((unused)) v62;
    uint64_t __attribute__((unused)) v63;
    uint64_t __attribute__((unused)) v64;
    uint64_t __attribute__((unused)) v65;
    uint64_t __attribute__((unused)) v66;
    uint64_t __attribute__((unused)) v67;
    uint64_t __attribute__((unused)) v68;
    uint64_t __attribute__((unused)) v69;
    uint64_t __attribute__((unused)) v70;
    uint64_t __attribute__((unused)) v71;
    uint64_t __attribute__((unused)) v72;
    uint64_t __attribute__((unused)) v73;
    uint64_t __attribute__((unused)) v74;
    uint64_t __attribute__((unused)) v75;
    uint64_t __attribute__((unused)) v76;
    uint64_t __attribute__((unused)) v77;
    uint64_t __attribute__((unused)) v78;
    uint64_t __attribute__((unused)) v79;
    uint64_t __attribute__((unused)) v80;
    uint64_t __attribute__((unused)) v81;
    uint64_t __attribute__((unused)) v82;
    uint64_t __attribute__((unused)) v83;
    uint64_t __attribute__((unused)) v84;
    uint64_t __attribute__((unused)) v85;
    uint64_t __attribute__((unused)) v86;
    uint64_t __attribute__((unused)) v87;
    uint64_t __attribute__((unused)) v88;
    uint64_t __attribute__((unused)) v89;
    uint64_t __attribute__((unused)) v90;
    uint64_t __attribute__((unused)) v91;
    uint64_t __attribute__((unused)) v92;
    uint64_t __attribute__((unused)) v93;
    uint64_t __attribute__((unused)) v94;
    uint64_t __attribute__((unused)) v95;
    uint64_t __attribute__((unused)) v96;
    uint64_t __attribute__((unused)) v97;
    uint64_t __attribute__((unused)) v98;
    uint64_t __attribute__((unused)) v99;
    v0 = p0;
    v2 = 0llu;
    v3 = ((int64_t)v0 >= (int64_t)v2) ? 1 : 0;
    v4 = 37792llu;
    v5 = ((int64_t)v0 < (int64_t)v4) ? 1 : 0;
    v6 = (v3 && v5) ? 1 : 0;
    if (v6) {
        v1 = 97llu;
        v99 = v1;
    }
    else {
        v8 = 37792llu;
        v9 = ((int64_t)v0 >= (int64_t)v8) ? 1 : 0;
        v10 = 54588llu;
        v11 = ((int64_t)v0 < (int64_t)v10) ? 1 : 0;
        v12 = (v9 && v11) ? 1 : 0;
        if (v12) {
            v7 = 99llu;
            v98 = v7;
        }
        else {
            v14 = 54588llu;
            v15 = ((int64_t)v0 >= (int64_t)v14) ? 1 : 0;
            v16 = 71384llu;
            v17 = ((int64_t)v0 < (int64_t)v16) ? 1 : 0;
            v18 = (v15 && v17) ? 1 : 0;
            if (v18) {
                v13 = 103llu;
                v97 = v13;
            }
            else {
                v20 = 71384llu;
                v21 = ((int64_t)v0 >= (int64_t)v20) ? 1 : 0;
                v22 = 109176llu;
                v23 = ((int64_t)v0 < (int64_t)v22) ? 1 : 0;
                v24 = (v21 && v23) ? 1 : 0;
                if (v24) {
                    v19 = 116llu;
                    v96 = v19;
                }
                else {
                    v26 = 109176llu;
                    v27 = ((int64_t)v0 >= (int64_t)v26) ? 1 : 0;
                    v28 = 111975llu;
                    v29 = ((int64_t)v0 < (int64_t)v28) ? 1 : 0;
                    v30 = (v27 && v29) ? 1 : 0;
                    if (v30) {
                        v25 = 66llu;
                        v95 = v25;
                    }
                    else {
                        v32 = 111975llu;
                        v33 = ((int64_t)v0 >= (int64_t)v32) ? 1 : 0;
                        v34 = 114774llu;
                        v35 = ((int64_t)v0 < (int64_t)v34) ? 1 : 0;
                        v36 = (v33 && v35) ? 1 : 0;
                        if (v36) {
                            v31 = 68llu;
                            v94 = v31;
                        }
                        else {
                            v38 = 114774llu;
                            v39 = ((int64_t)v0 >= (int64_t)v38) ? 1 : 0;
                            v40 = 117574llu;
                            v41 = ((int64_t)v0 < (int64_t)v40) ? 1 : 0;
                            v42 = (v39 && v41) ? 1 : 0;
                            if (v42) {
                                v37 = 72llu;
                                v93 = v37;
                            }
                            else {
                                v44 = 117574llu;
                                v45 = ((int64_t)v0 >= (int64_t)v44) ? 1 : 0;
                                v46 = 120373llu;
                                v47 = ((int64_t)v0 < (int64_t)v46) ? 1 : 0;
                                v48 = (v45 && v47) ? 1 : 0;
                                if (v48) {
                                    v43 = 75llu;
                                    v92 = v43;
                                }
                                else {
                                    v50 = 120373llu;
                                    v51 = ((int64_t)v0 >= (int64_t)v50) ? 1 : 0;
                                    v52 = 123172llu;
                                    v53 = ((int64_t)v0 < (int64_t)v52) ? 1 : 0;
                                    v54 = (v51 && v53) ? 1 : 0;
                                    if (v54) {
                                        v49 = 77llu;
                                        v91 = v49;
                                    }
                                    else {
                                        v56 = 123172llu;
                                        v57 = ((int64_t)v0 >= (int64_t)v56) ? 1 : 0;
                                        v58 = 125972llu;
                                        v59 = ((int64_t)v0 < (int64_t)v58) ? 1 : 0;
                                        v60 = (v57 && v59) ? 1 : 0;
                                        if (v60) {
                                            v55 = 78llu;
                                            v90 = v55;
                                        }
                                        else {
                                            v62 = 125972llu;
                                            v63 = ((int64_t)v0 >= (int64_t)v62) ? 1 : 0;
                                            v64 = 128771llu;
                                            v65 = ((int64_t)v0 < (int64_t)v64) ? 1 : 0;
                                            v66 = (v63 && v65) ? 1 : 0;
                                            if (v66) {
                                                v61 = 82llu;
                                                v89 = v61;
                                            }
                                            else {
                                                v68 = 128771llu;
                                                v69 = ((int64_t)v0 >= (int64_t)v68) ? 1 : 0;
                                                v70 = 131570llu;
                                                v71 = ((int64_t)v0 < (int64_t)v70) ? 1 : 0;
                                                v72 = (v69 && v71) ? 1 : 0;
                                                if (v72) {
                                                    v67 = 83llu;
                                                    v88 = v67;
                                                }
                                                else {
                                                    v74 = 131570llu;
                                                    v75 = ((int64_t)v0 >= (int64_t)v74) ? 1 : 0;
                                                    v76 = 134370llu;
                                                    v77 = ((int64_t)v0 < (int64_t)v76) ? 1 : 0;
                                                    v78 = (v75 && v77) ? 1 : 0;
                                                    if (v78) {
                                                        v73 = 86llu;
                                                        v87 = v73;
                                                    }
                                                    else {
                                                        v80 = 134370llu;
                                                        v81 = ((int64_t)v0 >= (int64_t)v80) ? 1 : 0;
                                                        v82 = 137169llu;
                                                        v83 = ((int64_t)v0 < (int64_t)v82) ? 1 : 0;
                                                        v84 = (v81 && v83) ? 1 : 0;
                                                        if (v84) {
                                                            v79 = 87llu;
                                                            v86 = v79;
                                                        }
                                                        else {
                                                            v85 = 89llu;
                                                            v86 = v85;
                                                        }
                                                        v87 = v86;
                                                    }
                                                    v88 = v87;
                                                }
                                                v89 = v88;
                                            }
                                            v90 = v89;
                                        }
                                        v91 = v90;
                                    }
                                    v92 = v91;
                                }
                                v93 = v92;
                            }
                            v94 = v93;
                        }
                        v95 = v94;
                    }
                    v96 = v95;
                }
                v97 = v96;
            }
            v98 = v97;
        }
        v99 = v98;
    }
    return v99;
}

uint64_t pick_homo_codepoint(uint64_t p0) {
    uint64_t __attribute__((unused)) v0;
    uint64_t __attribute__((unused)) v1;
    uint64_t __attribute__((unused)) v2;
    uint64_t __attribute__((unused)) v3;
    uint64_t __attribute__((unused)) v4;
    uint64_t __attribute__((unused)) v5;
    uint64_t __attribute__((unused)) v6;
    uint64_t __attribute__((unused)) v7;
    uint64_t __attribute__((unused)) v8;
    uint64_t __attribute__((unused)) v9;
    uint64_t __attribute__((unused)) v10;
    uint64_t __attribute__((unused)) v11;
    uint64_t __attribute__((unused)) v12;
    uint64_t __attribute__((unused)) v13;
    uint64_t __attribute__((unused)) v14;
    uint64_t __attribute__((unused)) v15;
    uint64_t __attribute__((unused)) v16;
    uint64_t __attribute__((unused)) v17;
    uint64_t __attribute__((unused)) v18;
    uint64_t __attribute__((unused)) v19;
    uint64_t __attribute__((unused)) v20;
    uint64_t __attribute__((unused)) v21;
    uint64_t __attribute__((unused)) v22;
    v0 = p0;
    v2 = 0llu;
    v3 = ((int64_t)v0 >= (int64_t)v2) ? 1 : 0;
    v4 = 42404llu;
    v5 = ((int64_t)v0 < (int64_t)v4) ? 1 : 0;
    v6 = (v3 && v5) ? 1 : 0;
    if (v6) {
        v1 = 97llu;
        v22 = v1;
    }
    else {
        v8 = 42404llu;
        v9 = ((int64_t)v0 >= (int64_t)v8) ? 1 : 0;
        v10 = 70117llu;
        v11 = ((int64_t)v0 < (int64_t)v10) ? 1 : 0;
        v12 = (v9 && v11) ? 1 : 0;
        if (v12) {
            v7 = 99llu;
            v21 = v7;
        }
        else {
            v14 = 70117llu;
            v15 = ((int64_t)v0 >= (int64_t)v14) ? 1 : 0;
            v16 = 97767llu;
            v17 = ((int64_t)v0 < (int64_t)v16) ? 1 : 0;
            v18 = (v15 && v17) ? 1 : 0;
            if (v18) {
                v13 = 103llu;
                v20 = v13;
            }
            else {
                v19 = 116llu;
                v20 = v19;
            }
            v21 = v20;
        }
        v22 = v21;
    }
    return v22;
}

void write_repeat_section(uint64_t p0, uint64_t p1, uint64_t p2) {
    uint64_t __attribute__((unused)) v0;
    uint64_t __attribute__((unused)) v1;
    uint64_t __attribute__((unused)) v2;
    uint64_t __attribute__((unused)) v3;
    uint64_t __attribute__((unused)) v5;
    uint64_t __attribute__((unused)) v6;
    uint64_t __attribute__((unused)) v8;
    uint64_t __attribute__((unused)) v9;
    uint64_t __attribute__((unused)) v10;
    uint64_t __attribute__((unused)) v11;
    uint64_t __attribute__((unused)) v12;
    uint64_t __attribute__((unused)) v13;
    uint64_t __attribute__((unused)) v14;
    uint64_t __attribute__((unused)) v15;
    uint64_t __attribute__((unused)) v16;
    uint64_t __attribute__((unused)) v17;
    uint64_t __attribute__((unused)) v18;
    uint64_t __attribute__((unused)) v19;
    uint64_t __attribute__((unused)) v20;
    uint64_t __attribute__((unused)) v21;
    uint64_t __attribute__((unused)) v22;
    uint64_t __attribute__((unused)) v23;
    uint64_t __attribute__((unused)) v24;
    uint64_t __attribute__((unused)) v25;
    uint64_t __attribute__((unused)) v26;
    uint64_t __attribute__((unused)) v27;
    uint64_t __attribute__((unused)) v28;
    uint64_t __attribute__((unused)) v29;
    uint64_t __attribute__((unused)) v30;
    uint64_t __attribute__((unused)) v31;
    uint64_t __attribute__((unused)) v32;
    uint64_t __attribute__((unused)) v33;
    uint64_t __attribute__((unused)) v35;
    uint64_t __attribute__((unused)) v36;
    uint64_t __attribute__((unused)) v37;
    uint64_t __attribute__((unused)) v38;
    uint64_t __attribute__((unused)) v39;
    uint64_t __attribute__((unused)) v40;
    uint64_t __attribute__((unused)) v41;
    uint64_t __attribute__((unused)) v42;
    uint64_t __attribute__((unused)) v43;
    uint64_t __attribute__((unused)) v44;
    uint64_t __attribute__((unused)) v45;
    uint64_t __attribute__((unused)) v46;
    uint64_t __attribute__((unused)) v48;
    uint64_t __attribute__((unused)) v49;
    uint64_t __attribute__((unused)) v51;
    uint64_t __attribute__((unused)) v52;
    uint64_t __attribute__((unused)) v53;
    uint64_t __attribute__((unused)) v54;
    uint64_t __attribute__((unused)) v55;
    uint64_t __attribute__((unused)) v56;
    uint64_t __attribute__((unused)) v57;
    uint64_t __attribute__((unused)) v58;
    uint64_t __attribute__((unused)) v59;
    uint64_t __attribute__((unused)) v60;
    uint64_t __attribute__((unused)) v61;
    uint64_t __attribute__((unused)) TextBuilder_local_0;
    uint64_t __attribute__((unused)) I32_local_1;
    uint64_t __attribute__((unused)) I32_local_2;
    uint64_t __attribute__((unused)) I32_local_3;
    v0 = p0;
    v1 = p1;
    v2 = p2;
    sarif_stdout_write((const unsigned char*)v0);
    v3 = 1llu;
    if (v3) {
    }
    static unsigned char _text_5[] = {
        1u, 0u, 0u, 0u, 0u, 0u, 0u, 0u /* len=1 */,10u,
    };
    v5 = (uint64_t)(unsigned char*)_text_5;
    sarif_stdout_write((const unsigned char*)v5);
    v6 = 1llu;
    if (v6) {
    }
    v8 = sarif_text_len((const unsigned char*)v1);
    v9 = (uint64_t)sarif_text_builder_new();
    TextBuilder_local_0 = v9;
    v10 = 0llu;
    I32_local_1 = v10;
    v11 = 0llu;
    I32_local_2 = v11;
    I32_local_3 = v2;
    while (1) {
        v12 = I32_local_3;
        v13 = 0llu;
        v14 = ((int64_t)v12 > (int64_t)v13) ? 1 : 0;
        if (!(v14)) break;
        v15 = I32_local_3;
        v16 = 60llu;
        v17 = ((int64_t)v15 < (int64_t)v16) ? 1 : 0;
        if (v17) {
            v18 = I32_local_3;
            v20 = v18;
        }
        else {
            v19 = 60llu;
            v20 = v19;
        }
        v21 = I32_local_2;
        v22 = v21 + v20;
        v23 = ((int64_t)v22 <= (int64_t)v8) ? 1 : 0;
        if (v23) {
            v24 = TextBuilder_local_0;
            v25 = I32_local_2;
            v26 = (uint64_t)sarif_text_builder_append_slice((void*)v24, (const unsigned char*)v1, (int64_t)v25, (int64_t)v22);
            TextBuilder_local_0 = v26;
        }
        else {
            v27 = TextBuilder_local_0;
            v28 = I32_local_2;
            v29 = (uint64_t)sarif_text_builder_append_slice((void*)v27, (const unsigned char*)v1, (int64_t)v28, (int64_t)v8);
            TextBuilder_local_0 = v29;
            v30 = TextBuilder_local_0;
            v31 = 0llu;
            v32 = v22 - v8;
            v33 = (uint64_t)sarif_text_builder_append_slice((void*)v30, (const unsigned char*)v1, (int64_t)v31, (int64_t)v32);
            TextBuilder_local_0 = v33;
        }
        v35 = TextBuilder_local_0;
        v36 = 10llu;
        v37 = (uint64_t)sarif_text_builder_append_ascii((void*)v35, (int64_t)v36);
        TextBuilder_local_0 = v37;
        v38 = I32_local_1;
        v39 = 1llu;
        v40 = v38 + v39;
        I32_local_1 = v40;
        v41 = I32_local_1;
        v42 = 4096llu;
        v43 = (v41 == v42) ? 1 : 0;
        if (v43) {
            v44 = TextBuilder_local_0;
            v45 = (uint64_t)sarif_stdout_write_builder((void*)v44);
            v46 = 1llu;
            if (v46) {
            }
            v48 = (uint64_t)sarif_text_builder_new();
            TextBuilder_local_0 = v48;
            v49 = 0llu;
            I32_local_1 = v49;
        }
        v51 = I32_local_2;
        v52 = v51 + v20;
        v53 = (int64_t)v52 / (int64_t)v8;
        v54 = v53 * v8;
        v55 = v52 - v54;
        I32_local_2 = v55;
        v56 = I32_local_3;
        v57 = v56 - v20;
        I32_local_3 = v57;
    }
    v59 = TextBuilder_local_0;
    v60 = (uint64_t)sarif_stdout_write_builder((void*)v59);
    v61 = 1llu;
    if (v61) {
    }
    return v62;
}

uint64_t write_random_section(uint64_t p0, uint64_t p1, uint64_t p2, uint64_t p3) {
    uint64_t __attribute__((unused)) v0;
    uint64_t __attribute__((unused)) v1;
    uint64_t __attribute__((unused)) v2;
    uint64_t __attribute__((unused)) v3;
    uint64_t __attribute__((unused)) v4;
    uint64_t __attribute__((unused)) v6;
    uint64_t __attribute__((unused)) v7;
    uint64_t __attribute__((unused)) v9;
    uint64_t __attribute__((unused)) v10;
    uint64_t __attribute__((unused)) v11;
    uint64_t __attribute__((unused)) v12;
    uint64_t __attribute__((unused)) v13;
    uint64_t __attribute__((unused)) v14;
    uint64_t __attribute__((unused)) v15;
    uint64_t __attribute__((unused)) v16;
    uint64_t __attribute__((unused)) v17;
    uint64_t __attribute__((unused)) v18;
    uint64_t __attribute__((unused)) v19;
    uint64_t __attribute__((unused)) v20;
    uint64_t __attribute__((unused)) v21;
    uint64_t __attribute__((unused)) v22;
    uint64_t __attribute__((unused)) v23;
    uint64_t __attribute__((unused)) v24;
    uint64_t __attribute__((unused)) v25;
    uint64_t __attribute__((unused)) v26;
    uint64_t __attribute__((unused)) v27;
    uint64_t __attribute__((unused)) v28;
    uint64_t __attribute__((unused)) v29;
    uint64_t __attribute__((unused)) v30;
    uint64_t __attribute__((unused)) v31;
    uint64_t __attribute__((unused)) v32;
    uint64_t __attribute__((unused)) v33;
    uint64_t __attribute__((unused)) v34;
    uint64_t __attribute__((unused)) v35;
    uint64_t __attribute__((unused)) v36;
    uint64_t __attribute__((unused)) v37;
    uint64_t __attribute__((unused)) v38;
    uint64_t __attribute__((unused)) v39;
    uint64_t __attribute__((unused)) v40;
    uint64_t __attribute__((unused)) v41;
    uint64_t __attribute__((unused)) v42;
    uint64_t __attribute__((unused)) v43;
    uint64_t __attribute__((unused)) v44;
    uint64_t __attribute__((unused)) v45;
    uint64_t __attribute__((unused)) v46;
    uint64_t __attribute__((unused)) v47;
    uint64_t __attribute__((unused)) v49;
    uint64_t __attribute__((unused)) v50;
    uint64_t __attribute__((unused)) v52;
    uint64_t __attribute__((unused)) v53;
    uint64_t __attribute__((unused)) v54;
    uint64_t __attribute__((unused)) v55;
    uint64_t __attribute__((unused)) v56;
    uint64_t __attribute__((unused)) v57;
    uint64_t __attribute__((unused)) v59;
    uint64_t __attribute__((unused)) I32_local_0;
    uint64_t __attribute__((unused)) TextBuilder_local_1;
    uint64_t __attribute__((unused)) I32_local_2;
    uint64_t __attribute__((unused)) I32_local_3;
    uint64_t __attribute__((unused)) I32_local_4;
    v0 = p0;
    v1 = p1;
    v2 = p2;
    v3 = p3;
    sarif_stdout_write((const unsigned char*)v1);
    v4 = 1llu;
    if (v4) {
    }
    static unsigned char _text_6[] = {
        1u, 0u, 0u, 0u, 0u, 0u, 0u, 0u /* len=1 */,10u,
    };
    v6 = (uint64_t)(unsigned char*)_text_6;
    sarif_stdout_write((const unsigned char*)v6);
    v7 = 1llu;
    if (v7) {
    }
    I32_local_0 = v0;
    v9 = (uint64_t)sarif_text_builder_new();
    TextBuilder_local_1 = v9;
    v10 = 0llu;
    I32_local_2 = v10;
    I32_local_3 = v2;
    while (1) {
        v11 = I32_local_3;
        v12 = 0llu;
        v13 = ((int64_t)v11 > (int64_t)v12) ? 1 : 0;
        if (!(v13)) break;
        v14 = I32_local_3;
        v15 = 60llu;
        v16 = ((int64_t)v14 < (int64_t)v15) ? 1 : 0;
        if (v16) {
            v17 = I32_local_3;
            v19 = v17;
        }
        else {
            v18 = 60llu;
            v19 = v18;
        }
        v20 = 0llu;
        I32_local_4 = v20;
        while (1) {
            v21 = I32_local_4;
            v22 = ((int64_t)v21 < (int64_t)v19) ? 1 : 0;
            if (!(v22)) break;
            v24 = I32_local_0;
            v23 = (uint64_t)next_seed(v24);
            I32_local_0 = v23;
            v25 = TextBuilder_local_1;
            if (v3) {
                v27 = I32_local_0;
                v26 = (uint64_t)pick_homo_codepoint(v27);
                v30 = v26;
            }
            else {
                v29 = I32_local_0;
                v28 = (uint64_t)pick_iub_codepoint(v29);
                v30 = v28;
            }
            v31 = (uint64_t)sarif_text_builder_append_ascii((void*)v25, (int64_t)v30);
            TextBuilder_local_1 = v31;
            v32 = I32_local_4;
            v33 = 1llu;
            v34 = v32 + v33;
            I32_local_4 = v34;
        }
        v36 = TextBuilder_local_1;
        v37 = 10llu;
        v38 = (uint64_t)sarif_text_builder_append_ascii((void*)v36, (int64_t)v37);
        TextBuilder_local_1 = v38;
        v39 = I32_local_2;
        v40 = 1llu;
        v41 = v39 + v40;
        I32_local_2 = v41;
        v42 = I32_local_2;
        v43 = 4096llu;
        v44 = (v42 == v43) ? 1 : 0;
        if (v44) {
            v45 = TextBuilder_local_1;
            v46 = (uint64_t)sarif_stdout_write_builder((void*)v45);
            v47 = 1llu;
            if (v47) {
            }
            v49 = (uint64_t)sarif_text_builder_new();
            TextBuilder_local_1 = v49;
            v50 = 0llu;
            I32_local_2 = v50;
        }
        v52 = I32_local_3;
        v53 = v52 - v19;
        I32_local_3 = v53;
    }
    v55 = TextBuilder_local_1;
    v56 = (uint64_t)sarif_stdout_write_builder((void*)v55);
    v57 = 1llu;
    if (v57) {
    }
    v59 = I32_local_0;
    return v59;
}

void sarif_user_main(void) {
    uint64_t __attribute__((unused)) v0;
    uint64_t __attribute__((unused)) v1;
    uint64_t __attribute__((unused)) v2;
    uint64_t __attribute__((unused)) v3;
    uint64_t __attribute__((unused)) v4;
    uint64_t __attribute__((unused)) v5;
    uint64_t __attribute__((unused)) v6;
    uint64_t __attribute__((unused)) v7;
    uint64_t __attribute__((unused)) v9;
    uint64_t __attribute__((unused)) v10;
    uint64_t __attribute__((unused)) v11;
    uint64_t __attribute__((unused)) v12;
    uint64_t __attribute__((unused)) v13;
    uint64_t __attribute__((unused)) v14;
    uint64_t __attribute__((unused)) v15;
    uint64_t __attribute__((unused)) v16;
    uint64_t __attribute__((unused)) v17;
    uint64_t __attribute__((unused)) v18;
    uint64_t __attribute__((unused)) v19;
    uint64_t __attribute__((unused)) v20;
    uint64_t __attribute__((unused)) v21;
    uint64_t __attribute__((unused)) v22;
    uint64_t __attribute__((unused)) v23;
    v0 = sarif_arg_count();
    v1 = 1llu;
    v2 = ((int64_t)v0 > (int64_t)v1) ? 1 : 0;
    if (v2) {
        v3 = 1llu;
        v4 = (uint64_t)sarif_arg_text((int64_t)v3);
        v5 = (uint64_t)sarif_parse_i32((const unsigned char*)v4);
        v7 = v5;
    }
    else {
        v6 = 250000llu;
        v7 = v6;
    }
    static unsigned char _text_9[] = {
        21u, 0u, 0u, 0u, 0u, 0u, 0u, 0u /* len=21 */,62u,79u,78u,69u,32u,72u,111u,109u,111u,32u,115u,97u,112u,105u,101u,110u,
        115u,32u,97u,108u,117u,
    };
    v9 = (uint64_t)(unsigned char*)_text_9;
    static unsigned char _text_10[] = {
        31u, 1u, 0u, 0u, 0u, 0u, 0u, 0u /* len=287 */,71u,71u,67u,67u,71u,71u,71u,67u,71u,67u,71u,71u,84u,71u,71u,67u,
        84u,67u,65u,67u,71u,67u,67u,84u,71u,84u,65u,65u,84u,67u,67u,67u,
        65u,71u,67u,65u,67u,84u,84u,84u,71u,71u,71u,65u,71u,71u,67u,67u,
        71u,65u,71u,71u,67u,71u,71u,71u,67u,71u,71u,65u,84u,67u,65u,67u,
        67u,84u,71u,65u,71u,71u,84u,67u,65u,71u,71u,65u,71u,84u,84u,67u,
        71u,65u,71u,65u,67u,67u,65u,71u,67u,67u,84u,71u,71u,67u,67u,65u,
        65u,67u,65u,84u,71u,71u,84u,71u,65u,65u,65u,67u,67u,67u,67u,71u,
        84u,67u,84u,67u,84u,65u,67u,84u,65u,65u,65u,65u,65u,84u,65u,67u,
        65u,65u,65u,65u,65u,84u,84u,65u,71u,67u,67u,71u,71u,71u,67u,71u,
        84u,71u,71u,84u,71u,71u,67u,71u,67u,71u,67u,71u,67u,67u,84u,71u,
        84u,65u,65u,84u,67u,67u,67u,65u,71u,67u,84u,65u,67u,84u,67u,71u,
        71u,71u,65u,71u,71u,67u,84u,71u,65u,71u,71u,67u,65u,71u,71u,65u,
        71u,65u,65u,84u,67u,71u,67u,84u,84u,71u,65u,65u,67u,67u,67u,71u,
        71u,71u,65u,71u,71u,67u,71u,71u,65u,71u,71u,84u,84u,71u,67u,65u,
        71u,84u,71u,65u,71u,67u,67u,71u,65u,71u,65u,84u,67u,71u,67u,71u,
        67u,67u,65u,67u,84u,71u,67u,65u,67u,84u,67u,67u,65u,71u,67u,67u,
        84u,71u,71u,71u,67u,71u,65u,67u,65u,71u,65u,71u,67u,71u,65u,71u,
        65u,67u,84u,67u,67u,71u,84u,67u,84u,67u,65u,65u,65u,65u,65u,
    };
    v10 = (uint64_t)(unsigned char*)_text_10;
    v11 = 2llu;
    v12 = v7 * v11;
    write_repeat_section(v9, v10, v12);
    v14 = 42llu;
    static unsigned char _text_15[] = {
        24u, 0u, 0u, 0u, 0u, 0u, 0u, 0u /* len=24 */,62u,84u,87u,79u,32u,73u,85u,66u,32u,97u,109u,98u,105u,103u,117u,105u,
        116u,121u,32u,99u,111u,100u,101u,115u,
    };
    v15 = (uint64_t)(unsigned char*)_text_15;
    v16 = 3llu;
    v17 = v7 * v16;
    v18 = 0llu;
    v13 = (uint64_t)write_random_section(v14, v15, v17, v18);
    static unsigned char _text_20[] = {
        29u, 0u, 0u, 0u, 0u, 0u, 0u, 0u /* len=29 */,62u,84u,72u,82u,69u,69u,32u,72u,111u,109u,111u,32u,115u,97u,112u,105u,
        101u,110u,115u,32u,102u,114u,101u,113u,117u,101u,110u,99u,121u,
    };
    v20 = (uint64_t)(unsigned char*)_text_20;
    v21 = 5llu;
    v22 = v7 * v21;
    v23 = 1llu;
    v19 = (uint64_t)write_random_section(v13, v20, v22, v23);
}
const struct SarifEffectHandler sarif_effect_table[1] = { {0, 0, 0} };
const size_t sarif_effect_table_len = 0;
