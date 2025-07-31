


for plot in plot_names:
    src = os.path.join(plot_dir, plot)
    dst = os.path.join(output_dir, plot)
    if os.path.exists(src):
        shutil.copyfile(src, dst)
        print(f"✅ Copied {plot} to report_outputs/")
    else:
        print(f"[WARNING] Plot file not found: {src}")