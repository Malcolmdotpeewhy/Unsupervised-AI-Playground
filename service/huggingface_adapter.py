import logging
from model_downloader import HFPlaygroundDownloader

class HuggingFaceAdapterLayer:
    def __init__(self, hf_token=None):
        self.downloader = HFPlaygroundDownloader(hf_token)

    def evaluate_execution_engine(self, repo_id: str) -> dict:
        """
        Takes a HuggingFace repo and determines its required 
        backend, execution engine, architecture, and pipeline_tag.
        """
        try:
            metadata = self.downloader.probe_type(repo_id)
            
            pipeline = metadata.get("pipeline_tag") or ""
            architectures = metadata.get("architectures", [])
            model_type = metadata.get("model_type", "")
            tags = metadata.get("tags", [])
            
            backend = "unknown"
            engine = "unknown"
            
            # GGUF evaluation -> llama_cpp
            if "gguf" in tags or any(t.endswith(".gguf") for t in tags):
                backend = "llama_cpp"
                engine = "GGML"
            # OpenVINO evaluation -> openvino
            elif "openvino" in tags or any(t.endswith("-ov") for t in tags):
                backend = "openvino"
                engine = "OpenVINO"
            # Stable Diffusion / ComfyUI capabilities
            elif pipeline in ["text-to-image", "image-to-image"] or "StableDiffusion" in tags or any("StableDiffusion" in a for a in architectures):
                backend = "comfyui"
                engine = "Diffusers"
            elif "stable-diffusion" in tags or "stable-diffusion-xl" in tags:
                backend = "comfyui"
                engine = "Diffusers"
            # Transfomers fallback
            elif pipeline in ["text-generation", "feature-extraction"] or "transformers" in tags:
                backend = "transformers"
                engine = "Transformers"

            arch = architectures[0] if architectures else model_type
                
            return {
                "backend": backend,
                "engine": engine,
                "architecture": arch,
                "pipeline_tag": pipeline,
                "success": backend != "unknown",
            }
        except Exception as ex:
            logging.error(f"AdapterLayer evaluation failed for {repo_id}: {ex}")
            return {
                "backend": "unknown",
                "engine": "unknown",
                "architecture": "unknown",
                "pipeline_tag": "unknown",
                "success": False,
                "error": str(ex)
            }
