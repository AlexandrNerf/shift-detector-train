import hydra
from omegaconf import DictConfig
from ultralytics import YOLO, settings


@hydra.main(config_path='config', config_name='config.yaml', version_base='1.2.0')
def main(cfg: DictConfig):
    print('Args:', cfg)

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
