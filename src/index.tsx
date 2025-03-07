import { PLUGIN_NAME } from "./helpers/commonDefs";
import { definePlugin } from "@decky/api";
import { FaSave } from "react-icons/fa";
import ApiClient from "./helpers/apiClient";
import { Content } from "./pages/quickAccessMenu";
import PluginLogsPage from "./pages/pluginLogsPage";
import ConfigCloudPage from "./pages/configCloudPage";

export default definePlugin(() => {
  const registrationArray: Array<Unregisterable> = [];

  registrationArray.push(ApiClient.setupAppLifetimeNotificationsHandler());
  registrationArray.push(ApiClient.setupScreenshotNotification());

  registrationArray.push(PluginLogsPage.register());
  registrationArray.push(ConfigCloudPage.register());

  return {
    name: PLUGIN_NAME,
    content: <Content />,
    icon: <FaSave />,
    onDismount() {
      registrationArray.forEach(registration => registration.unregister());
    }
  }
});
