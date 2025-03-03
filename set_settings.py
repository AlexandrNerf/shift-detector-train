import hydra
from omegaconf import DictConfig
from ultralytics import settings


@hydra.main(config_path='config', config_name='config.yaml', version_base='1.2.0')
def update_settings(cfg: DictConfig):
    # Setting all loggers with config
    settings.update(
            {
                'datasets_dir': '',
                'mlflow': cfg.logger.mlflow,
                'wandb': cfg.logger.wandb,
                'tensorboard': cfg.logger.tensorboard,
                'clearml': cfg.logger.clearml,
                'comet': cfg.logger.comet,
                'dvc': cfg.logger.dvc,
                'hub': cfg.logger.hub,
                'neptune': cfg.logger.neptune,
                'raytune': cfg.logger.raytune,
                'vscode_msg': cfg.logger.vscode_msg,
            }
        )
    print(f'You successfully changed loggers\nSettings you set: \n{cfg.logger}')
    
if __name__ == '__main__':
    update_settings()