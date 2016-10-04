# coding: utf-8

import sys
import re

def main(fname, dirname):
    noise_e = re.compile("</siteinfo>")
    noise_b = re.compile("</mediawiki>")
    page_s = re.compile("<page>")
    page_g = re.compile("</page>")
    noise = True

    with open(fname, "r") as f:
        out_sub = 0
        text = ""
        text_n = 0
        line_n = 0

        for line in f:
            line_n += 1
            if line_n % 10000000 == 0:
                sys.stderr.write("{0:010d}\n".format(line_n))
                sys.stderr.flush()
            if noise_e.search(line):
                noise = False
                continue
            elif noise_b.search(line):
                noise = True
                continue

            if noise:
                continue

            text += line
            if page_s.search(line):
                text_n += 1
            elif page_g.search(line):
                if text_n >= 10000:
                    text_n = 0
                    with open(dirname + "/{0:04d}.xml".format(out_sub), "w") as out:
                        out.write("<wiki>\n")
                        out.write(text)
                        out.write("</wiki>\n")
                    out_sub += 1
                    text = ""

        if len(text) > 0:
            with open(dirname + "/{0:04d}.xml".format(out_sub), "w") as out:
                out.write("<wiki>\n")
                out.write(text)
                out.write("</wiki>\n")

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
