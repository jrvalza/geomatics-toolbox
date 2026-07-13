
path_input_file = "cameras_metashape.txt"
path_output_file = "cameras_matlab.csv"

with open (path_input_file, 'r') as file:
    data = file.readlines()
    out = open(path_output_file, "w")
    out.write(f"id;xUTM;yUTM;H;omega;phi;kappa\n")
    for line in data:
        row = line.strip().split()
        try:
            id = row[0]
            xUTM = row[1]
            yUTM = row[2]
            H = row[3]
            omega = row[4]
            phi = row[5]
            kappa = row[6]
            out.write(f"{str(id)};{round(float(xUTM),3)};{round(float(yUTM),3)};{round(float(H),3)};{round(float(omega),6)};{round(float(phi),6)};{round(float(kappa),6)}\n")
        except:
            pass
    out.close()
    