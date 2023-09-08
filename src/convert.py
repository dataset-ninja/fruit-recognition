# https://www.kaggle.com/datasets/chrisfilo/fruit-recognition

import glob
import os
import shutil
from urllib.parse import unquote, urlparse

import numpy as np
import supervisely as sly
from dotenv import load_dotenv
from supervisely.io.fs import (
    file_exists,
    get_file_name,
    get_file_name_with_ext,
    get_file_size,
)
from tqdm import tqdm

import src.settings as s
from dataset_tools.convert import unpack_if_archive


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(desc=f"Downloading '{file_name_with_ext}' to buffer...", total=fsize) as pbar:
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path


def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    # project_name = "Fruit Recognition"
    images_path = "/mnt/d/datasetninja-raw/fruit-recognition"
    ds_name = "ds"
    batch_size = 30

    contain_subfolders = ["Apple", "Guava", "Kiwi"]
    duplicates_folders = [
        "Total Number of Apples",
        "Guava total",
        "guava total final",
        "Total Number of Kiwi fruit",
    ]

    def create_ann(image_path, fruit_folder_):
        labels = []
        tags = []

        image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = image_np.shape[0]
        img_wight = image_np.shape[1]

        fruit = sly.Tag(meta.get_tag_meta(fruit_folder_.lower()))
        tags.append(fruit)

        possible_subfolder = image_path.split("/")[-2]
        if possible_subfolder != fruit_folder_:
            subfolder_tag = sly.Tag(tag_subfolder_data, value=possible_subfolder)
            tags.append(subfolder_tag)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=tags)

    tag_apple = sly.TagMeta("apple", sly.TagValueType.NONE)
    tag_banana = sly.TagMeta("banana", sly.TagValueType.NONE)
    tag_carambola = sly.TagMeta("carambola", sly.TagValueType.NONE)
    tag_guava = sly.TagMeta("guava", sly.TagValueType.NONE)
    tag_kiwi = sly.TagMeta("kiwi", sly.TagValueType.NONE)
    tag_mango = sly.TagMeta("mango", sly.TagValueType.NONE)
    tag_muskmelon = sly.TagMeta("muskmelon", sly.TagValueType.NONE)
    tag_orange = sly.TagMeta("orange", sly.TagValueType.NONE)
    tag_peach = sly.TagMeta("peach", sly.TagValueType.NONE)
    tag_pear = sly.TagMeta("pear", sly.TagValueType.NONE)
    tag_persimmon = sly.TagMeta("persimmon", sly.TagValueType.NONE)
    tag_pitaya = sly.TagMeta("pitaya", sly.TagValueType.NONE)
    tag_plum = sly.TagMeta("plum", sly.TagValueType.NONE)
    tag_pomegranate = sly.TagMeta("pomegranate", sly.TagValueType.NONE)
    tag_tomatoes = sly.TagMeta("tomatoes", sly.TagValueType.NONE)
    tag_subfolder_data = sly.TagMeta("sub-category", sly.TagValueType.ANY_STRING)

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(
        tag_metas=[
            tag_apple,
            tag_banana,
            tag_carambola,
            tag_guava,
            tag_kiwi,
            tag_mango,
            tag_muskmelon,
            tag_orange,
            tag_peach,
            tag_pear,
            tag_persimmon,
            tag_pitaya,
            tag_plum,
            tag_pomegranate,
            tag_tomatoes,
            tag_subfolder_data,
        ],
    )
    api.project.update_meta(project.id, meta.to_json())

    dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

    for fruit_folder in os.listdir(images_path):
        curr_images_path = os.path.join(images_path, fruit_folder)
        if fruit_folder in contain_subfolders:
            for subfolder in os.listdir(curr_images_path):
                if subfolder in duplicates_folders:
                    continue
                sub_images_path = os.path.join(curr_images_path, subfolder)
                images_names = os.listdir(sub_images_path)

                progress = sly.Progress(
                    "Create dataset {}, add {} data".format(ds_name, subfolder), len(images_names)
                )

                for img_names_batch in sly.batched(images_names, batch_size=batch_size):
                    images_pathes_batch = [
                        os.path.join(sub_images_path, image_path) for image_path in img_names_batch
                    ]

                    if fruit_folder == "Apple":
                        prefix = subfolder.split(" ")[1]
                        if prefix != "Number":
                            img_names_batch = [
                                prefix + "_" + im_name for im_name in img_names_batch
                            ]

                    img_infos = api.image.upload_paths(
                        dataset.id, img_names_batch, images_pathes_batch
                    )
                    img_ids = [im_info.id for im_info in img_infos]

                    anns_batch = [
                        create_ann(image_path, fruit_folder) for image_path in images_pathes_batch
                    ]
                    api.annotation.upload_anns(img_ids, anns_batch)

                    progress.iters_done_report(len(img_names_batch))

        else:
            images_names = os.listdir(curr_images_path)

            progress = sly.Progress(
                "Create dataset {}, add {} data".format(ds_name, fruit_folder), len(images_names)
            )

            for img_names_batch in sly.batched(images_names, batch_size=batch_size):
                images_pathes_batch = [
                    os.path.join(curr_images_path, image_path) for image_path in img_names_batch
                ]

                img_infos = api.image.upload_paths(dataset.id, img_names_batch, images_pathes_batch)
                img_ids = [im_info.id for im_info in img_infos]

                anns_batch = [
                    create_ann(image_path, fruit_folder) for image_path in images_pathes_batch
                ]
                api.annotation.upload_anns(img_ids, anns_batch)

                progress.iters_done_report(len(img_names_batch))
    return project
