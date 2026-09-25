import os

def fix_mojibake_str(s):
    result = []
    buffer = bytearray()
    
    for char in s:
        try:
            # Try to encode using cp1252
            b = char.encode('cp1252')
            buffer.extend(b)
        except UnicodeEncodeError:
            # Not cp1252 encodable (e.g. correct Persian or other unicode)
            if buffer:
                try:
                    result.append(buffer.decode('utf-8'))
                except UnicodeDecodeError:
                    # If decoding fails, fallback to cp1252
                    result.append(buffer.decode('cp1252', errors='replace'))
                buffer = bytearray()
            result.append(char)
            
    if buffer:
        try:
            result.append(buffer.decode('utf-8'))
        except UnicodeDecodeError:
            result.append(buffer.decode('cp1252', errors='replace'))
            
    return "".join(result)

def fix_mojibake(directory):
    repaired_count = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.po'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for classic double-encoding signs
                if 'Ø' in content or 'Ù' in content:
                    print(f"Repairing Mojibake in: {filepath}")
                    try:
                        fixed_content = fix_mojibake_str(content)
                        with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
                            f.write(fixed_content)
                        repaired_count += 1
                        print(f"Successfully repaired: {filepath}")
                    except Exception as e:
                        print(f"Failed to repair {filepath}: {e}")
                        
    print(f"Total files successfully repaired: {repaired_count}")

if __name__ == '__main__':
    fix_mojibake(r'c:\omp-server\Local_Overrides')
