import {
  ButtonItem,
  definePlugin,
  DialogButton,
  Menu,
  MenuItem,
  PanelSection,
  PanelSectionRow,
  Router,
  ServerAPI,
  showContextMenu,
  staticClasses,
} from "decky-frontend-lib";
import { useState, VFC } from "react";
import { FaShip } from "react-icons/fa";

import logo from "../assets/logo.png";

interface AddMethodArgs {
  left: number;
  right: number;
}

const Content: VFC<{ serverAPI: ServerAPI }> = ({ serverAPI }) => {
  const [rr, setResult] = useState<any>(0);

  const openConfig = async (backend: "onedrive") => {
    const response = await serverAPI.callPluginMethod<{ backend_type: "onedrive" }, string>("spawn", { backend_type: backend });
    if (response.success) {
      Router.CloseSideMenus();
      Router.NavigateToExternalWeb(response.result);
    } else {
      console.error(response.result);
    }
  };

  const onClick = async () => {
    const result = await serverAPI.callPluginMethod<AddMethodArgs, number>("add", {
      left: rr,
      right: 2,
    });
    if (result.success) {
      setResult(result.result);
    }
  };

  return (
    <PanelSection title="Panel Section">
      <PanelSectionRow>
        Close browser after configuration completes.
        <ButtonItem
          layout="below"
          onClick={(e) =>
            showContextMenu(
              <Menu label="Menu" cancelText="Cancel" onCancel={() => {}}>
                <MenuItem onSelected={() => openConfig("onedrive")}>OneDrive</MenuItem>
              </Menu>,
              e.currentTarget ?? window
            )
          }
        >
          Configure
        </ButtonItem>
        <ButtonItem layout="below" onClick={() => onClick()}>
          {JSON.stringify(debug)}
        </ButtonItem>
      </PanelSectionRow>

      <PanelSectionRow>
        <div style={{ display: "flex", justifyContent: "center" }}>
          <img src={logo} />
        </div>
      </PanelSectionRow>

      <PanelSectionRow>
        <ButtonItem
          layout="below"
          onClick={() => {
            Router.CloseSideMenus();
            Router.Navigate("/decky-plugin-test");
          }}
        >
          Router
        </ButtonItem>
      </PanelSectionRow>
    </PanelSection>
  );
};

const DeckyPluginRouterTest: VFC = () => {
  return (
    <div style={{ marginTop: "50px", color: "white" }}>
      Hello World!
      <DialogButton onClick={() => Router.NavigateToChat()}>Go to Chat</DialogButton>
    </div>
  );
};

export default definePlugin((serverApi: ServerAPI) => {
  serverApi.routerHook.addRoute("/decky-plugin-test", DeckyPluginRouterTest, {
    exact: true,
  });

  return {
    title: <div className={staticClasses.Title}>Example Plugin</div>,
    content: <Content serverAPI={serverApi} />,
    icon: <FaShip />,
    onDismount() {
      serverApi.routerHook.removeRoute("/decky-plugin-test");
    },
  };
});
