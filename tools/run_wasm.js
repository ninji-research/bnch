const fs = require('fs');

if (process.argv.length < 3) {
    console.error("Usage: node run_wasm.js <path.wasm> [args...]");
    process.exit(1);
}

const wasmPath = process.argv[2];
const args = process.argv.slice(2); // argv[0] is the binary name/path

let stdinBuffer = null;
function getStdinBuffer() {
    if (stdinBuffer === null) {
        try {
            stdinBuffer = fs.readFileSync(0); // read all stdin lazily
        } catch (e) {
            stdinBuffer = Buffer.alloc(0);
        }
    }
    return stdinBuffer;
}

let wasmMemory = null;

const imports = {
    wasi_snapshot_preview1: {
        fd_write: (fd, iovs, iovs_len, nwritten_ptr) => {
            if (fd !== 1) return 8;
            const mem = new Uint8Array(wasmMemory.buffer);
            const view = new DataView(wasmMemory.buffer);
            let totalWritten = 0;
            for (let i = 0; i < iovs_len; i++) {
                const base = iovs + i * 8;
                const ptr = view.getInt32(base, true);
                const len = view.getInt32(base + 4, true);
                if (len < 0) return 21;
                const slice = mem.slice(ptr, ptr + len);
                process.stdout.write(slice);
                totalWritten += len;
            }
            if (nwritten_ptr !== 0) {
                view.setInt32(nwritten_ptr, totalWritten, true);
            }
            return 0;
        }
    },
    env: {
        __host_argc: () => {
            return BigInt(args.length);
        },
        __host_argv: (index, buf_ptr, buf_len) => {
            const idx = Number(index);
            if (idx < 0 || idx >= args.length) return -1;
            const argBytes = Buffer.from(args[idx], 'utf-8');
            const to_copy = Math.min(argBytes.length, buf_len);
            const mem = new Uint8Array(wasmMemory.buffer);
            argBytes.copy(mem, buf_ptr, 0, to_copy);
            return to_copy;
        },
        __host_stdin_read: (buf_ptr, buf_len) => {
            if (buf_ptr < 0 || buf_len < 0) return -1;
            const buf = getStdinBuffer();
            const to_copy = Math.min(buf.length, buf_len);
            const mem = new Uint8Array(wasmMemory.buffer);
            buf.copy(mem, buf_ptr, 0, to_copy);
            return to_copy;
        }
    }
};

const wasmBytes = fs.readFileSync(wasmPath);
WebAssembly.instantiate(wasmBytes, imports)
    .then(result => {
        wasmMemory = result.instance.exports.memory;
        if (result.instance.exports.main) {
            const exitCode = result.instance.exports.main();
            if (exitCode !== undefined) {
                const val = BigInt(exitCode);
                const upper = val >> 32n;
                const lower = val & 0xFFFFFFFFn;
                if (upper !== 0n && upper !== 0xFFFFFFFFn && upper !== -1n) {
                    const ptr = Number(lower);
                    const len = Number(upper);
                    const mem = new Uint8Array(wasmMemory.buffer);
                    const bytes = mem.slice(ptr, ptr + len);
                    process.stdout.write(bytes);
                    process.exit(0);
                } else {
                    console.log(val.toString());
                    process.exit(0);
                }
            } else {
                process.exit(0);
            }
        } else if (result.instance.exports._start) {
            result.instance.exports._start();
        } else {
            console.error("No main or _start export found in WebAssembly module");
            process.exit(1);
        }
    })
    .catch(err => {
        console.error("Failed to run WebAssembly:", err);
        process.exit(1);
    });
