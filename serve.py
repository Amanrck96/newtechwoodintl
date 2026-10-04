import http.server
import socketserver
import os
import sys
import re

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class RangeRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def send_head(self):
        path = self.translate_path(self.path)
        if os.path.isdir(path):
            return super().send_head()
            
        ctype = self.guess_type(path)
        try:
            f = open(path, 'rb')
        except OSError:
            self.send_error(404, 'File not found')
            return None
            
        fs = os.fstat(f.fileno())
        total_length = fs.st_size
        
        range_header = self.headers.get('Range')
        if range_header and range_header.startswith('bytes='):
            m = re.match(r'bytes=(\d*)-(\d*)', range_header)
            if m:
                first_byte_str, last_byte_str = m.groups()
                if first_byte_str and last_byte_str:
                    start = int(first_byte_str)
                    end = int(last_byte_str)
                elif first_byte_str:
                    start = int(first_byte_str)
                    end = total_length - 1
                elif last_byte_str:
                    end = total_length - 1
                    start = max(0, total_length - int(last_byte_str))
                else:
                    start = 0
                    end = total_length - 1
                    
                if 0 <= start <= end < total_length:
                    self.send_response(206, 'Partial Content')
                    self.send_header('Content-Type', ctype)
                    self.send_header('Content-Range', f'bytes {start}-{end}/{total_length}')
                    self.send_header('Content-Length', str(end - start + 1))
                    self.send_header('Accept-Ranges', 'bytes')
                    self.end_headers()
                    f.seek(start)
                    self.range_end = end
                    return f
                    
        self.send_response(200)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(total_length))
        self.send_header('Accept-Ranges', 'bytes')
        self.end_headers()
        self.range_end = total_length - 1
        return f

    def copyfile(self, source, outputfile):
        if not hasattr(self, 'range_end'):
            return super().copyfile(source, outputfile)
        start = source.tell()
        bytes_to_send = self.range_end - start + 1
        buffer_size = 64 * 1024
        while bytes_to_send > 0:
            chunk = source.read(min(bytes_to_send, buffer_size))
            if not chunk:
                break
            try:
                outputfile.write(chunk)
            except (ConnectionResetError, BrokenPipeError):
                break
            bytes_to_send -= len(chunk)

    def log_message(self, format, *args):
        # Clean logging
        sys.stderr.write("%s - - [%s] %s\n" %
                         (self.address_string(),
                          self.log_date_time_string(),
                          format % args))

class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True

def main():
    sys.stdout.reconfigure(line_buffering=True)
    with ThreadingTCPServer(("", PORT), RangeRequestHandler) as httpd:
        print(f"Local server started at http://localhost:{PORT}")
        print("Supporting HTTP 206 Range Requests & Multi-Threading.")
        print("Press Ctrl+C to stop the server.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopping server...")

if __name__ == '__main__':
    main()
