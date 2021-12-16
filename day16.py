inputs = []
inputs.append("""420D598021E0084A07C98EC91DCAE0B880287912A925799429825980593D7DCD400820329480BF21003CC0086028910097520230C80813401D8CC00F601881805705003CC00E200E98400F50031801D160048E5AFEFD5E5C02B93F2F4C11CADBBB799CB294C5FDB8E12C40139B7C98AFA8B2600DCBAF4D3A4C27CB54EA6F5390B1004B93E2F40097CA2ECF70C1001F296EF9A647F5BFC48C012C0090E675DF644A675DF645A7E6FE600BE004872B1B4AAB5273ED601D2CD240145F802F2CFD31EFBD4D64DD802738333992F9FFE69CAF088C010E0040A5CC65CD25774830A80372F9D78FA4F56CB6CDDC148034E9B8D2F189FD002AF3918AECD23100953600900021D1863142400043214C668CB31F073005A6E467600BCB1F4B1D2805930092F99C69C6292409CE6C4A4F530F100365E8CC600ACCDB75F8A50025F2361C9D248EF25B662014870035600042A1DC77890200D41086B0FE4E918D82CC015C00DCC0010F8FF112358002150DE194529E9F7B9EE064C015B005C401B8470F60C080371460CC469BA7091802F39BE6252858720AC2098B596D40208A53CBF3594092FF7B41B3004A5DB25C864A37EF82C401C9BCFE94B7EBE2D961892E0C1006A32C4160094CDF53E1E4CDF53E1D8005FD3B8B7642D3B4EB9C4D819194C0159F1ED00526B38ACF6D73915F3005EC0179C359E129EFDEFEEF1950005988E001C9C799ABCE39588BB2DA86EB9ACA22840191C8DFBE1DC005EE55167EFF89510010B322925A7F85A40194680252885238D7374C457A6830C012965AE00D4C40188B306E3580021319239C2298C4ED288A1802B1AF001A298FD53E63F54B7004A68B25A94BEBAAA00276980330CE0942620042E3944289A600DC388351BDC00C9DCDCFC8050E00043E2AC788EE200EC2088919C0010A82F0922710040F289B28E524632AE0""")

inputs.append("D8005AC2A8F0")
inputs.append("CE00C43D881120")
inputs.append("880086C3E88112")
inputs.append("04005AC33890")
inputs.append("C200B40A82")
inputs.append("8A004A801A8002F478")
inputs.append("620080001611562C8802118E34")
inputs.append("C0015000016115A2E0802F182340")
inputs.append("A0016C880162017C3686B18A3D4780")


line = inputs[0]

def to_binary(hexl):
    s = ''
    for char in hexl:
        if (char == '0'):
            s += '0000'
        elif (char == '1'):
            s += '0001'
        elif (char == '2'):
            s += '0010'
        elif (char == '3'):
            s += '0011'
        elif (char == '4'):
            s += '0100'
        elif (char == '5'):
            s += '0101'
        elif (char == '6'):
            s += '0110'
        elif (char == '7'):
            s += '0111'
        elif (char == '8'):
            s += '1000'
        else:
            s += format(int(char, 16), 'b')
    return s
    
binary_string_repr = ''

for char in line:
    binary_string_repr += to_binary(char)


def get_sum(packet):
    version = int(packet[0:3], 2)
    type_id = int(packet[3:6], 2)
    if type_id != 4:
        length_type_id = packet[6]
        values = []
        next_idx = None
        if length_type_id == '1':
            num_sub_packet = int(packet[7:18], 2)
            next_idx = 18
            for i in range(num_sub_packet):
                sti = packet[next_idx:]
                v_sum, offset = get_sum(sti)
                values.append(v_sum)
                next_idx += offset
                version += v_sum
        elif length_type_id == '0':
            sub_packet_bits = int(packet[7:22], 2)
            next_idx = 22 
            offset = 0
            offset_sum = 0
            while offset_sum < sub_packet_bits:
                v_sum, offset = get_sum(packet[next_idx: next_idx + sub_packet_bits - offset])
                values.append(v_sum)
                version += v_sum
                next_idx += offset
                offset_sum += offset

        # eval
        if type_id == 0:
            return sum(values), next_idx
        if type_id == 1:
            return reduce(lambda a, b: a * b, values), next_idx
        if type_id == 2:
            return min(values), next_idx
        if type_id == 3:
            return max(values), next_idx
        if type_id == 5:
            return 1 if values[0] > values[1] else 0, next_idx
        if type_id == 6:
            return 1 if values[0] < values[1] else 0, next_idx
        if type_id == 7:
            return 1 if values[0] == values[1] else 0, next_idx
    else:
        pos = 6
        leading_bit = packet[pos]
        pos += 1
        value = packet[pos:pos+4]
        pos += 4 
        while leading_bit != '0':
            leading_bit = packet[pos]
            pos += 1
            value += packet[pos:pos+4]
            pos += 4 
        return int(value, 2), pos


print get_sum(to_binary(line))

