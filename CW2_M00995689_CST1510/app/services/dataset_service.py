from app.data.datasets import (
    insert_dataset, get_all_datasets, get_datasets_by_department,
    update_dataset, delete_dataset
)

def create_dataset(**kwargs):
    return insert_dataset(**kwargs)

def list_datasets():
    return get_all_datasets()

def list_datasets_by_department(department):
    return get_datasets_by_department(department)

def modify_dataset(dataset_id, **kwargs):
    update_dataset(dataset_id, **kwargs)

def remove_dataset(dataset_id):
    delete_dataset(dataset_id)