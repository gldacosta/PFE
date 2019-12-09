def number_of_vector_changes(new_vector, current_vector) -> int :
    number_of_changes = new_vector ^ current_vector
    return str(bin(number_of_changes)).count("1")

with open("./data.vcd","r") as file:
    enddefinitions = False

    tokeniser = (word for line in file for word in line.split() if word)

    variables = dict()
    changes = 0
    clock = 0

    for count,token in enumerate(tokeniser):
        if not enddefinitions:
       # definition section

            if token == "$dumpvars":
                print("End def")
                enddefinitions = True
        else:
            # get first char of the token 
            # c = it is used to check if the token is a vector or clock or other
            # rest = all characters after the first one 
            # example b10101001 c = b rest = 10101001
            # example #630 c = # rest = 630  
            c, rest = token[0], token[1:]
            
            if c == '#' and rest.isdigit(): # its a clock period
                new_clock = int(rest)
                if new_clock - clock >= 1260:
                    print(f"From {clock} to {new_clock} there were {changes} changes")
                    changes = 0
                    clock = new_clock
                
            elif c == 'b':
                # here we know it is a binary vector
                
                # x not in rest =>  drops vectors that have x anywhere in the vector
                # len(token) > 1 => drops variable named b
                # rest.isdigit() => drops variables like b! or b, 
                if "x" not in rest and len(token) > 1 and rest.isdigit():   
                    
                    vector = int(rest, 2)
                    var = next(tokeniser)
    
                    if var in variables:
                        changes += number_of_vector_changes(vector, variables[var])
                        variables[var] = vector
                    else:
                        variables[var] = vector