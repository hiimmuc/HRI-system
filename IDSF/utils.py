import logging
import os
import random
from re import S

import numpy as np
import torch
from seqeval.metrics import f1_score, precision_score, recall_score
from transformers import (AlbertConfig, AlbertTokenizer, BertConfig,
                          BertTokenizer, DistilBertConfig, DistilBertTokenizer)

try:
    from model import JointAlbert, JointBERT, JointDistilBERT
except ModuleNotFoundError:
    from IDSF.model import JointAlbert, JointBERT, JointDistilBERT


MODEL_CLASSES = {
    'bert': (BertConfig, JointBERT, BertTokenizer),
    'distilbert': (DistilBertConfig, JointDistilBERT, DistilBertTokenizer),
    'albert': (AlbertConfig, JointAlbert, AlbertTokenizer)
}

MODEL_PATH_MAP = {
    'bert': 'bert-base-uncased',
    'distilbert': 'distilbert-base-uncased',
    'albert': 'albert-xxlarge-v1'
}


def get_intent_labels(args):
    return [label.strip() for label in open(os.path.join(args.data_dir, args.task, args.intent_label_file), 'r', encoding='utf-8')]


def get_slot_labels(args):
    return [label.strip() for label in open(os.path.join(args.data_dir, args.task, args.slot_label_file), 'r', encoding='utf-8')]


def load_tokenizer(args):
    return MODEL_CLASSES[args.model_type][2].from_pretrained(args.model_name_or_path)


def init_logger():
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                        datefmt='%m/%d/%Y %H:%M:%S',
                        level=logging.INFO)


def set_seed(args):
    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    if not args.no_cuda and torch.cuda.is_available():
        torch.cuda.manual_seed_all(args.seed)


def compute_metrics(intent_preds, intent_labels, slot_preds, slot_labels):
    assert len(intent_preds) == len(intent_labels) == len(
        slot_preds) == len(slot_labels)
    results = {}
    intent_result = get_intent_acc(intent_preds, intent_labels)
    slot_result = get_slot_metrics(slot_preds, slot_labels)
    sementic_result = get_sentence_frame_acc(
        intent_preds, intent_labels, slot_preds, slot_labels)

    results.update(intent_result)
    results.update(slot_result)
    results.update(sementic_result)

    return results


def get_slot_metrics(preds, labels):
    assert len(preds) == len(labels)
    return {
        "slot_precision": precision_score(labels, preds),
        "slot_recall": recall_score(labels, preds),
        "slot_f1": f1_score(labels, preds)
    }


def get_intent_acc(preds, labels):
    acc = (preds == labels).mean()
    return {
        "intent_acc": acc
    }


def read_prediction_text(args):
    return [text.strip() for text in open(os.path.join(args.pred_dir, args.pred_input_file), 'r', encoding='utf-8')]


def get_sentence_frame_acc(intent_preds, intent_labels, slot_preds, slot_labels):
    """For the cases that intent and all the slots are correct (in one sentence)"""
    # Get the intent comparison result
    intent_result = (intent_preds == intent_labels)

    # Get the slot comparision result
    slot_result = []
    for preds, labels in zip(slot_preds, slot_labels):
        assert len(preds) == len(labels)
        one_sent_result = True
        for p, l in zip(preds, labels):
            if p != l:
                one_sent_result = False
                break
        slot_result.append(one_sent_result)
    slot_result = np.array(slot_result)

    sementic_acc = np.multiply(intent_result, slot_result).mean()
    return {
        "sementic_frame_acc": sementic_acc
    }


def evaluate_results(args, intent_outputs, slot_outputs, use_crf=False):
    '''run evaluate the output of model to get the prediction results

    Args:
        args ([type]): [description]
        model ([type]): [description]
        inputs ([type]): [description]
        intent_logits ([type]): [description]
        slot_logits ([type]): [description]
        use_crf (bool, optional): [description]. Defaults to False.

    Returns:
        [tuple]: total results including intent, slot, and sementic frame accuracy
    '''

    intent_preds, out_intent_label_ids = intent_outputs
    slot_preds, out_slot_labels_ids = slot_outputs

    pad_token_label_id = args.ignore_index
    slot_label_lst = get_slot_labels(args)

    # Intent result
    intent_preds = np.argmax(intent_preds, axis=1)

    # Slot result
    if not use_crf:
        slot_preds = np.argmax(slot_preds, axis=2)
    slot_label_map = {i: label for i, label in enumerate(slot_label_lst)}
    out_slot_label_list = [[] for _ in range(out_slot_labels_ids.shape[0])]
    slot_preds_list = [[] for _ in range(out_slot_labels_ids.shape[0])]

    for i in range(out_slot_labels_ids.shape[0]):
        for j in range(out_slot_labels_ids.shape[1]):
            if out_slot_labels_ids[i, j] != pad_token_label_id:
                out_slot_label_list[i].append(slot_label_map[out_slot_labels_ids[i][j]])
                slot_preds_list[i].append(slot_label_map[slot_preds[i][j]])

    total_result = compute_metrics(intent_preds, out_intent_label_ids, slot_preds_list, out_slot_label_list)

    return total_result
