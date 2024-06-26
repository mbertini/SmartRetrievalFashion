import pickle
import os
import argparse
import json

from fashion_clip.fashion_clip import FashionCLIP, FCLIPDataset
from data_utilis import dataset_root, server_base_path, get_url


def parse_args():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-v', '--verbose', action='store_true', help='increase output verbosity')
    parser.add_argument('file', metavar='F', type=str, default=str(dataset_root / 'dataset.json'),
                        help='JSON file describing all the datasets to be processed')
    return parser.parse_args()


def main(args):
    dataset_file = args.file
    if args.verbose:
        print(f"Opening the dataset JSON file: {dataset_file}")
    f = open(dataset_file)
    datasets_json = json.load(f)
    fclip = FashionCLIP('fashion-clip')
    for dataset in datasets_json:
        single_dataset_file = str(server_base_path) + os.sep + dataset['metadata_path']
        f = open(single_dataset_file, encoding="utf8")
        single_dataset_json = json.load(f)
        catalog = []
        images = []
        for j in single_dataset_json:
            image_path = str(server_base_path) + os.sep + str(dataset['image_path']) + os.sep + str(
                j['article_id']) + ".jpg"
            catalog.append({'id': j['article_id'], 'image': image_path, 'caption': j['detail_desc']})
            images.append(image_path)
        if args.verbose:
            print(f"Processing dataset: {dataset['name']} - {len(catalog)} images")
        images_embedded = fclip.encode_images(images, batch_size=8)
        output_pickle_filename = server_base_path + os.sep + dataset['fclip_path']
        with open(output_pickle_filename, 'wb+') as f:
            if args.verbose:
                print(f"Saving the embeddings to: {output_pickle_filename}")
            pickle.dump(images_embedded, f)


if __name__ == "__main__":
    print("Extracting FashionCLIP embeddings for the datasets.")
    args = parse_args()
    main(args)
    print("Done!")
