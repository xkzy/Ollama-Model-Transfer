import pytest
from unittest.mock import patch, MagicMock
from ModelManager import sanitize_filename_MF, run_command, create_ollama_model_file, scan_folder, process_models

def test_sanitize_filename_MF():
    assert sanitize_filename_MF("test:latest") == "test"
    assert sanitize_filename_MF("test<>:*?") == "test-----"

@patch("ModelManager.subprocess.Popen")
def test_run_command(mock_popen):
    # Test successful command
    mock_process = MagicMock()
    mock_process.communicate.return_value = ("hello\n", "")
    mock_popen.return_value = mock_process
    assert run_command("echo hello") == "hello"
    
    # Test command with stderr
    mock_process.communicate.return_value = ("", "error")
    assert run_command("invalid_command") == ""

from unittest.mock import patch

def test_create_ollama_model_file(tmp_path):
    model_name = "test_model"
    output_file = "ModelFile"
    BackUp_Folder = tmp_path / "backup"
    Ollama_Model_Folder = tmp_path / "models"

    with patch("ModelManager.run_command") as mock_run_command:
        mock_run_command.side_effect = [
            "template content",
            "parameter1\nparameter2", 
            "system message",
            "FROM /path/to/model.gguf",
        ]
        create_ollama_model_file(model_name, output_file, BackUp_Folder, Ollama_Model_Folder)
        
        target_file = BackUp_Folder / model_name / output_file
        assert target_file.exists()
        
        expected_content = '''FROM test_model.gguf
TEMPLATE """template content"""
PARAMETER parameter1
PARAMETER parameter2
system "system message"
'''
        assert target_file.read_text() == expected_content

@patch("ModelManager.os.walk")
@patch("ModelManager.subprocess.run")
def test_scan_folder(mock_run, mock_walk, tmp_path):
    mock_walk.return_value = [
        (str(tmp_path/"model"), [], ["test.gguf"])
    ]
    
    scan_folder(tmp_path)
    
    mock_run.assert_called_once_with(
        'ollama create model -f modelfile',
        shell=True,
        cwd=str(tmp_path/"model")
    )

@patch("ModelManager.create_ollama_model_file")
@patch("ModelManager.detect_ollama_model_folder")
def test_process_models(mock_detect, mock_create, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    mock_detect.return_value = str(tmp_path/"models")
    BackUp_Folder = tmp_path/"llama_backup"
    
    model_names = ["model1", "model2"]
    process_models(model_names)
    
    assert mock_create.call_count == 2
    mock_create.assert_any_call("model1", "ModelFile", "./llama_backup", str(tmp_path/"models"))
    mock_create.assert_any_call("model2", "ModelFile", "./llama_backup", str(tmp_path/"models"))