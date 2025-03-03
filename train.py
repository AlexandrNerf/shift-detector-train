import hydra
from omegaconf import DictConfig
from ultralytics import YOLO, settings


@hydra.main(config_path='config', config_name='config.yaml', version_base='1.2.0')
def main(cfg: DictConfig):
    print('Args:', cfg)

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

    model = YOLO(cfg.model)

    model.train(
        data=cfg.data,
        project=cfg.project,
        resume=cfg.resume,
        epochs=cfg.epochs,
        **cfg.hyperparams,
        **cfg.augmentations,
        **cfg.functional
    )


if __name__ == '__main__':
    main()
