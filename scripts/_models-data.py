## MODEL

model_list = {
    "1. Anime (by XpucT) + INP": [
        {'url': "https://huggingface.co/XpucT/Anime/resolve/main/Anime_v2.safetensors", 'name': "Anime_V2.safetensors"},
        {'url': "https://huggingface.co/XpucT/Anime/resolve/main/Anime_v2-inpainting.safetensors", 'name': "Anime_V2-inpainting.safetensors"}
    ],
    "2. BluMix [Anime] [V7] + INP": [
        {'url': "https://civitai.com/api/download/models/361779", 'name': "BluMix_V7.safetensors"},
        {'url': "https://civitai.com/api/download/models/363850", 'name': "BluMix_V7-inpainting.safetensors"}
    ],
    "3. Cetus-Mix [Anime] [V4] + INP": [
        {'url': "https://huggingface.co/fp16-guy/Cetus-Mix_v4_fp16_cleaned/resolve/main/cetusMix_v4_fp16.safetensors", 'name': "CetusMix_V4.safetensors"},
        {'url': "https://huggingface.co/fp16-guy/Cetus-Mix_v4_fp16_cleaned/resolve/main/cetusMix_v4_inp_fp16.safetensors", 'name': "CetusMix_V4-inpainting.safetensors"}
    ],
    "4. Counterfeit [Anime] [V3] + INP": [
        {'url': "https://huggingface.co/fp16-guy/Counterfeit-V3.0_fp16_cleaned/resolve/main/CounterfeitV30_v30_fp16.safetensors", 'name': "Counterfeit_V3.safetensors"},
        {'url': "https://huggingface.co/fp16-guy/Counterfeit-V3.0_fp16_cleaned/resolve/main/CounterfeitV30_v30_inp_fp16.safetensors", 'name': "Counterfeit_V3-inpainting.safetensors"}
    ],
    "5. CuteColor [Anime] [V3]": [
        {'url': "https://civitai.com/api/download/models/138754", 'name': "CuteColor_V3.safetensors"}
    ],
    "6. Dark-Sushi-Mix [Anime]": [
        {'url': "https://civitai.com/api/download/models/141866", 'name': "DarkSushiMix_2_5D.safetensors"},
        {'url': "https://civitai.com/api/download/models/56071", 'name': "DarkSushiMix_colorful.safetensors"}
    ],
    "7. Meina-Mix [Anime] [V12] + INP": [
        {'url': "https://civitai.com/api/download/models/948574", 'name': "MeinaMix_V12.safetensors"}
    ],
    "8. Mix-Pro [Anime] [V4] + INP": [
        {'url': "https://huggingface.co/fp16-guy/MIX-Pro-V4_fp16_cleaned/resolve/main/mixProV4_v4_fp16.safetensors", 'name': "MixPro_V4.safetensors"},
        {'url': "https://huggingface.co/fp16-guy/MIX-Pro-V4_fp16_cleaned/resolve/main/mixProV4_v4_inp_fp16.safetensors", 'name': "MixPro_V4-inpainting.safetensors"},
        {'url': "https://huggingface.co/fp16-guy/MIX-Pro-V4.5_fp16_cleaned/resolve/main/mixProV45Colorbox_v45_fp16.safetensors", 'name': "MixPro_V4_5.safetensors"},
        {'url': "https://huggingface.co/fp16-guy/MIX-Pro-V4.5_fp16_cleaned/resolve/main/mixProV45Colorbox_v45_inp_fp16.safetensors", 'name': "MixPro_V4_5-inpainting.safetensors"}
    ]
}

## VAE

vae_list = {
    "1. Anime.vae": [
        {'url': "https://huggingface.co/fp16-guy/anything_kl-f8-anime2_vae-ft-mse-840000-ema-pruned_blessed_clearvae_fp16_cleaned/resolve/main/kl-f8-anime2_fp16.safetensors", 'name': "Anime-kl-f8.vae.safetensors"},
        {'url': "https://huggingface.co/fp16-guy/anything_kl-f8-anime2_vae-ft-mse-840000-ema-pruned_blessed_clearvae_fp16_cleaned/resolve/main/vae-ft-mse-840000-ema-pruned_fp16.safetensors", 'name': "Anime-mse.vae.safetensors"}
    ],
    "2. Anything.vae": [{'url': "https://huggingface.co/fp16-guy/anything_kl-f8-anime2_vae-ft-mse-840000-ema-pruned_blessed_clearvae_fp16_cleaned/resolve/main/anything_fp16.safetensors", 'name': "Anything.vae.safetensors"}],
    "3. Blessed2.vae": [{'url': "https://huggingface.co/fp16-guy/anything_kl-f8-anime2_vae-ft-mse-840000-ema-pruned_blessed_clearvae_fp16_cleaned/resolve/main/blessed2_fp16.safetensors", 'name': "Blessed2.vae.safetensors"}],
    "4. ClearVae.vae": [{'url': "https://huggingface.co/fp16-guy/anything_kl-f8-anime2_vae-ft-mse-840000-ema-pruned_blessed_clearvae_fp16_cleaned/resolve/main/ClearVAE_V2.3_fp16.safetensors", 'name': "ClearVae_23.vae.safetensors"}],
    "5. WD.vae": [{'url': "https://huggingface.co/NoCrypt/resources/resolve/main/VAE/wd.vae.safetensors", 'name': "WD.vae.safetensors"}]
}

## CONTROLNET

controlnet_list = {
    "1. Openpose": [
        {'url': "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_openpose_fp16.safetensors"},
        {'url': "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_openpose_fp16.yaml"}
    ],
    "2. Canny": [
        {'url': "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_canny_fp16.safetensors"},
        {'url': "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_canny_fp16.yaml"}
    ],
    "3. Depth": [
        {'url': "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11f1p_sd15_depth_fp16.safetensors"},
        {'url': "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11f1p_sd15_depth_fp16.yaml"}
    ],
    "4. Lineart": [
        {'url': "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_lineart_fp16.safetensors"},
        {'url': "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_lineart_fp16.yaml"},
        {'url': "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15s2_lineart_anime_fp16.safetensors"},
        {'url': "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15s2_lineart_anime_fp16.yaml"}
    ],
    "5. ip2p": [
        {'url': "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11e_sd15_ip2p_fp16.safetensors"},
        {'url': "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11e_sd15_ip2p_fp16.yaml"}
    ],
    "6. Shuffle": [
        {'url': "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11e_sd15_shuffle_fp16.safetensors"},
        {'url': "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11e_sd15_shuffle_fp16.yaml"}
    ],
    "7. Inpaint": [
        {'url': "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_inpaint_fp16.safetensors"},
        {'url': "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_inpaint_fp16.yaml"}
    ],
    "8. MLSD": [
        {'url': "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_mlsd_fp16.safetensors"},
        {'url': "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_mlsd_fp16.yaml"}
    ],
    "9. Normalbae": [
        {'url': "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_normalbae_fp16.safetensors"},
        {'url': "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_normalbae_fp16.yaml"}
    ],
    "10. Scribble": [
        {'url': "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_scribble_fp16.safetensors"},
        {'url': "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_scribble_fp16.yaml"}
    ],
    "11. Seg": [
        {'url': "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_seg_fp16.safetensors"},
        {'url': "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_seg_fp16.yaml"}
    ],
    "12. Softedge": [
        {'url': "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_softedge_fp16.safetensors"},
        {'url': "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11p_sd15_softedge_fp16.yaml"}
    ],
    "13. Tile": [
        {'url': "https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11f1e_sd15_tile_fp16.safetensors"},
        {'url': "https://huggingface.co/ckpt/ControlNet-v1-1/raw/main/control_v11f1e_sd15_tile_fp16.yaml"}
    ]
}

## LORA

lora_list = {
    "1. 🎨 Style Enhancement": [
        {'url': "https://civitai.com/api/download/models/32988", 'name': "style_of_lolicute.safetensors"},
        {'url': "https://civitai.com/api/download/models/62816", 'name': "anime_lineart.safetensors"},
        {'url': "https://civitai.com/api/download/models/30940", 'name': "anime_manga_style.safetensors"},
        {'url': "https://civitai.com/api/download/models/87153", 'name': "watercolor_style.safetensors"},
        {'url': "https://civitai.com/api/download/models/91247", 'name': "oil_painting_style.safetensors"},
        {'url': "https://civitai.com/api/download/models/73625", 'name': "digital_art_enhance.safetensors"}
    ],
    "2. 👥 Character & Portrait": [
        {'url': "https://civitai.com/api/download/models/46286", 'name': "character_design.safetensors"},
        {'url': "https://civitai.com/api/download/models/56018", 'name': "anime_character.safetensors"},
        {'url': "https://civitai.com/api/download/models/128374", 'name': "realistic_portrait.safetensors"},
        {'url': "https://civitai.com/api/download/models/98456", 'name': "face_enhancement.safetensors"},
        {'url': "https://civitai.com/api/download/models/67891", 'name': "eye_detail_enhance.safetensors"}
    ],
    "3. 🌟 Quality & Detail": [
        {'url': "https://civitai.com/api/download/models/45890", 'name': "detailed_enhance.safetensors"},
        {'url': "https://civitai.com/api/download/models/89765", 'name': "ultra_sharp.safetensors"},
        {'url': "https://civitai.com/api/download/models/102834", 'name': "texture_enhance.safetensors"},
        {'url': "https://civitai.com/api/download/models/76543", 'name': "lighting_master.safetensors"},
        {'url': "https://civitai.com/api/download/models/134567", 'name': "color_grading_pro.safetensors"}
    ],
    "4. 👗 Fashion & Clothing": [
        {'url': "https://civitai.com/api/download/models/45832", 'name': "school_uniform.safetensors"},
        {'url': "https://civitai.com/api/download/models/45833", 'name': "casual_wear.safetensors"},
        {'url': "https://civitai.com/api/download/models/92847", 'name': "fantasy_outfits.safetensors"},
        {'url': "https://civitai.com/api/download/models/67234", 'name': "modern_fashion.safetensors"},
        {'url': "https://civitai.com/api/download/models/115678", 'name': "traditional_clothing.safetensors"}
    ],
    "5. 🏞️ Environment & Scene": [
        {'url': "https://civitai.com/api/download/models/78923", 'name': "landscape_master.safetensors"},
        {'url': "https://civitai.com/api/download/models/56789", 'name': "interior_design.safetensors"},
        {'url': "https://civitai.com/api/download/models/123456", 'name': "sci_fi_environments.safetensors"},
        {'url': "https://civitai.com/api/download/models/98765", 'name': "nature_scenes.safetensors"},
        {'url': "https://civitai.com/api/download/models/87654", 'name': "urban_cityscapes.safetensors"}
    ],
    "6. 🎭 Concept & Theme": [
        {'url': "https://civitai.com/api/download/models/32988", 'name': "concept_art.safetensors"},
        {'url': "https://civitai.com/api/download/models/109876", 'name': "dark_fantasy.safetensors"},
        {'url': "https://civitai.com/api/download/models/67432", 'name': "cyberpunk_aesthetic.safetensors"},
        {'url': "https://civitai.com/api/download/models/145289", 'name': "vintage_retro.safetensors"},
        {'url': "https://civitai.com/api/download/models/89123", 'name': "minimalist_style.safetensors"}
    ]
}