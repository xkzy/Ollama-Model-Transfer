import pytest
from ModelManager import sanitize_filename_MF, run_command, create_ollama_model_file, scan_folder, process_models

def test_sanitize_filename_MF():
    assert sanitize_filename_MF("test:latest") == "test"
    assert sanitize_filename_MF("test<>:*?") == "test-----"

def test_run_command():
    result = run_command("echo hello")
    assert result == "hello"

from unittest.mock import patch

def test_create_ollama_model_file(tmp_path):
    model_name = "test_model"
    output_file = "ModelFile"
    BackUp_Folder = tmp_path / "backup"
    Ollama_Model_Folder = tmp_path / "models"

    with patch("ModelManager.run_command") as mock_run_command:
        mock_run_command.side_effect = [
            "template content",  # Mock template
            "parameter1\nparameter2",  # Mock parameters
            "system message",  # Mock system message
            "FROM /path/to/model.gguf",  # Mock modelfile
        ]
        create_ollama_model_file(model_name, output_file, BackUp_Folder, Ollama_Model_Folder)
        assert (BackUp_Folder / model_name / output_file).exists()

def test_scan_folder(tmp_path):
    model_folder = tmp_path / "model"
    model_folder.mkdir()
    (model_folder / "test.gguf").touch()
    scan_folder(tmp_path)
    # Add assertions based on expected behavior

def test_process_models(tmp_path):
    model_names = ["model1", "model2"]
    process_models(model_names)
    # Add assertions based on expected behavior