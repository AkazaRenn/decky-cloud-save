import { ButtonItem, showContextMenu, Menu, MenuItem, showModal, ConfirmModal } from "@decky/ui";
import { FilePickerRes } from "@decky/api";
import { useState } from "react";
import { PageProps } from "../helpers/types";
import { Toast } from "../helpers/toast";

export default function AddNewPathButton({ serverApi, onPathAdded, file }: PageProps<{ onPathAdded?: () => void; file: "includes" | "excludes" }>) {
  const [buttonDisabled, setButtonDisabled] = useState(false);

  const onFileChosen = (res: FilePickerRes, mode: "file" | "directory" | "directory-norecurse") => {
    if (res.realpath === "/") {
      showModal(<ConfirmModal strTitle="Are you mad??" strDescription="For your own safety, ability to sync the whole file system is disabled" />);
      return;
    }

    setButtonDisabled(true);

    const path = mode === "directory" ? `${res.realpath}/**` : mode === "directory-norecurse" ? `${res.realpath}/*` : res.realpath;
    serverApi
      .callPluginMethod<{ path: string }, number>("test_syncpath", { path })
      .then((r: { success: any; result: any; }) => {
        if (!r.success) {
          Toast.toast(r.result);
          setButtonDisabled(false);
          return;
        }

        showModal(
          <ConfirmModal
            strTitle="Confirm Add"
            strDescription={`Path ${path} matches ${r.result} file(s). Proceed?`}
            onCancel={() => setButtonDisabled(false)}
            onEscKeypress={() => setButtonDisabled(false)}
            onOK={() => {
              serverApi
                .callPluginMethod<{ path: string; file: "includes" | "excludes" }, void>("add_syncpath", { path, file })
                .then(() => {
                  if (onPathAdded) onPathAdded();
                })
                .catch((e: any) => Toast.toast(e))
                .finally(() => setButtonDisabled(false));
            }}
          />
        );
      })
      .catch((e: any) => {
        Toast.toast(e);
        setButtonDisabled(false);
      });
  };

  return (
    <ButtonItem
      // icon={<FaPlus />}
      layout="below"
      onClick={() =>
        showContextMenu(
          <Menu label="Select Path to Sync">
            <MenuItem
              onSelected={() =>
                serverApi
                  .openFilePicker("/home/deck", true)
                  .then((e: any) => onFileChosen(e, "file"))
                  .catch()
              }
            >
              File
            </MenuItem>
            <MenuItem
              onSelected={() =>
                serverApi
                  .openFilePicker("/home/deck", false)
                  .then((e: any) => onFileChosen(e, "directory"))
                  .catch()
              }
            >
              Folder
            </MenuItem>
            <MenuItem
              onSelected={() =>
                serverApi
                  .openFilePicker("/home/deck", false)
                  .then((e: any) => onFileChosen(e, "directory-norecurse"))
                  .catch()
              }
            >
              Folder (exclude subfolders)
            </MenuItem>
          </Menu>
        )
      }
      disabled={buttonDisabled}
    >
      {file === "includes" ? "Add Path to Sync" : "Exclude Path from Sync"}
    </ButtonItem>
  );
}
