import { Navigate, Route, Routes } from "react-router-dom";

import { AdDetailPage } from "./pages/AdDetailPage";
import { CampaignPage } from "./pages/CampaignPage";

const App = () => {
  return (
    <Routes>
      <Route path="/" element={<CampaignPage />} />
      <Route path="/ads/:adId" element={<AdDetailPage />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
};

export default App;
