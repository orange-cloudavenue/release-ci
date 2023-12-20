
#! NOT THE GOOD SOLUTION !#
# EX 1
# codeObject = compile('string', 'changelog.py', 'exec')
# exec(codeObject)
# Output: 15

# EX 3
# codeInString = 'a = 5\nb=6\nmul=a*b\nprint("mul =",mul)'
# codeObject = compile(codeInString, 'multiplyNumbers', 'exec')
# exec(codeObject)

# EX 4
# tmpFile = open('changelog.py', 'r')
# tmpCode = tmpFile.read()
# tmpFile.close()
# codeObject = compile(tmpCode, 'testcode.py', 'exec')
# exec(codeObject)