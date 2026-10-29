import { Navigate, Route, Routes } from "react-router-dom";

import { AppLayout } from "./components/AppLayout/AppLayout";
import { AdDetailPage } from "./pages/AdDetailPage";
import { CampaignPage } from "./pages/CampaignPage";

const App = () => {
  return (
    <AppLayout>
      <Routes>
        <Route path="/" element={<CampaignPage />} />
        <Route path="/ads/:adId" element={<AdDetailPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </AppLayout>
  );
};

export default App;
