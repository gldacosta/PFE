#!python

from collections import Counter
from __future__ import with_statement
from itertools import dropwhile, takewhile, izip
from collections import defaultdict
from pprint import pprint as pp
import sys
 

vcdfile = ('teste.vcd','r')

class VCD(object):
   def __init__(self):
     self.scope = []
     self.idcode2references = defaultdict(list)
     self.reference2idcode = dict()
     self.enddefinitions = False
     self.id2stats = dict()  # Maps id to its accumulated statistics

   def textstats(self):
     total, updown, uponly, downonly = 0,0,0,0
     out = []
     for ref in sorted(self.reference2idcode.keys()):
       id = self.reference2idcode[ref]
       stats = self.id2stats[id]
       if stats.size == 1:
         total +=1
         if stats.zero2one and stats.one2zero:
           updown +=1
           covered = 'PASS'
         elif stats.zero2one:
           uponly +=1
           covered = 'FAIL0'
         elif stats.one2zero:
           downonly +=1
           covered = 'FAIL1'
         else:
           covered = 'FAIL10'
         out.append( "  %-50s %s" % ( '"'+".".join(x[1] for x in ref)+'":', (covered, stats.zero2one, stats.one2zero)) )
       else:
         total += stats.size
         for count, (one2zero, zero2one) in enumerate(izip(stats.one2zero, stats.zero2one)):
           if zero2one and one2zero:
             updown +=1
             covered = 'PASS'
           elif zero2one:
             uponly +=1
             covered = 'FAIL0'
           elif stats.one2zero:
             downonly +=1
             covered = 'FAIL1'
           else:
             covered = 'FAIL10'
           name = ".".join( x[1] for x in (ref+(('BIT:','<'+str(count)+'>'),)) )
           out.append( "  %-50s %s" % ( '"'+name+'":', (covered, zero2one, one2zero)) )
     header = "# TOGGLE REPORT: %g %%, %i / %i covered. %i up-only, %i down-only." % (
       updown/1.0/total*100, updown, total, uponly, downonly )
     body = "toggle={\n" + "\n".join(out) + '\n  }'
     return header, body
 
   def scaler_value_change(self, value, id):
     if value in '01' :
       stats = self.id2stats[id]
       if not stats.value:
         stats.value = value
       elif stats.value != value:
         stats.value = value
         if value == '0':
           stats.one2zero +=1
         else:
           stats.zero2one +=1
 
   def vector_value_change(self, format, number, id):
     if format == 'b':
       stats = self.id2stats[id]
       extend = stats.size - len(number)
       if extend:
         number = ('0' if number[0]=='1' else number[0])*extend + number
       newdigit, newone2zero, newzero2one = [],[],[]
       for digit, olddigit, one2zero, zero2one in izip(number, stats.value, stats.one2zero, stats.zero2one):
         if digit in '01' and olddigit and olddigit != digit:
           if digit == '0':
             one2zero +=1
           else:
             zero2one +=1
         elif digit not in '01':
           digit = olddigit
         newdigit.append(digit)
         newone2zero.append(one2zero)
         newzero2one.append(zero2one)
       stats.value, stats.one2zero, stats.zero2one = newdigit, newone2zero, newzero2one
 
 
class IdStats(object):
   def __init__(self, size):
     size = int(size)
     self.size = size
     if size ==1:
       self.value = ''
       self.zero2one = 0
       self.one2zero = 0
     else:
       # stats for each bit
       self.value       = ['' for x in range(size)]
       self.zero2one = [0 for x in range(size)]
       self.one2zero = [0 for x in range(size)]
   def __repr__(self):
     return "<IdStats: " + repr((self.size, self.value, self.zero2one, self.one2zero)) + ">"
 
 
vcd = VCD()
 
 def parse_error(tokeniser, keyword):
   raise "Don't understand keyword: " + keyword
 
 def drop_declaration(tokeniser, keyword):
   dropwhile(lambda x: x != "$end", tokeniser).next()
 
 def save_declaration(tokeniser, keyword):
   vcd.__setattr__(keyword.lstrip('$'),
                   " ".join( takewhile(lambda x: x != "$end", tokeniser)) )
 vcd_date      = save_declaration
 vcd_timescale = save_declaration
 vcd_version   = save_declaration
 
 def vcd_enddefinitions(tokeniser, keyword):
   vcd.enddefinitions = True
   drop_declaration(tokeniser, keyword)
   
 def vcd_scope(tokeniser, keyword):
   vcd.scope.append( tuple(takewhile(lambda x: x != "$end", tokeniser)))
 def vcd_upscope(tokeniser, keyword):
   vcd.scope.pop()
   tokeniser.next()
 def vcd_var(tokeniser, keyword):
   var_type, size, identifier_code, reference = tuple(takewhile(lambda x: x != "$end", tokeniser))
   reference = vcd.scope + [('var', reference)]
   vcd.idcode2references[identifier_code].append( (var_type, size, reference))
   vcd.reference2idcode[tuple(reference)] = identifier_code
   vcd.id2stats[identifier_code] = IdStats(size)
 def vcd_dumpall(tokeniser, keyword): pass
 def vcd_dumpoff(tokeniser, keyword): pass
 def vcd_dumpon(tokeniser, keyword): pass
 def vcd_dumpvars(tokeniser, keyword): pass
 def vcd_end(tokeniser, keyword):
   if not vcd.enddefinitions:
     parse_error(tokeniser, keyword)
 
 
 keyword2handler = {
   # declaration_keyword ::=
   "$comment":        drop_declaration,
   "$date":           vcd_date,
   "$enddefinitions": vcd_enddefinitions,
   "$scope":          vcd_scope,
   "$timescale":      vcd_timescale,
   "$upscope":        vcd_upscope,
   "$var":            vcd_var,
   "$version":        vcd_version,
   # simulation_keyword ::=
   "$dumpall":        vcd_dumpall,
   "$dumpoff":        vcd_dumpoff,
   "$dumpon":         vcd_dumpon,
   "$dumpvars":       vcd_dumpvars,
   "$end":            vcd_end,
   }
 keyword2handler = defaultdict(parse_error, keyword2handler)
 
 def vcd_toggle_count(vcdfile):
   f = open(vcdfile)
   tokeniser = (word for line in f for word in line.split() if word)
   for count,token in enumerate(tokeniser):
     if not vcd.enddefinitions:
       # definition section
       if token != '$var':
         print token
       keyword2handler[token](tokeniser, token)
     else:
       if count % 10000 == 0:
         print count, "\r",
       c, rest = token[0], token[1:]
       if c == '$':
         # skip $dump* tokens and $end tokens in sim section
         continue
       elif c == '#':
         vcd.now = rest
       elif c in '01xXzZ':
         vcd.scaler_value_change(value=c, id=rest)
       elif c in 'bBrR':
         vcd.vector_value_change(format=c.lower(), number=rest, id=tokeniser.next())
       else:
         raise "Don't understand: %s After %i words" % (token, count)
   print count
   f.close()
 
 vcd_toggle_count(vcdfile)
header, body = vcd.textstats()
print '\n'+header+'\n\n'+body+'\n'