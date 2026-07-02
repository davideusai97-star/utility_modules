import pickle
import sys
import pprint

'''
Prende in input un file .pkl (con percorso) ed una destinazione .txt
Rende leggibili i file .pkl, convertendoli in .txt
'''
def pkl_to_txt(input_file, output_path):
    try:
        with open(input_file, 'rb') as file:
            data = pickle.load(file)
        print("✅ Pickle file loaded successfully.")

    except FileNotFoundError:
        print(f"File not found: {input_file}")
    except pickle.UnpicklingError:
        print("Error: The file content is not a valid pickle format.")
    except EOFError:
        print("Error: The file is incomplete or corrupted.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    with open(output_path, "w") as f:
        pprint.pprint(data, stream=f, indent=2, width=120, sort_dicts=False)

if __name__ == "__main__":
    # Check for correct number of command-line arguments
    if len(sys.argv) != 3:
        print("Wrong number of arguments.")
        print("Usage: python convert_pkl_to_txt.py <path\input.pkl> <path\output.txt>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    pkl_to_txt(input_file, output_file)