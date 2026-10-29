import "./PageState.scss";

type PageLoadingProps = {
  label: string;
};

export const PageLoading = ({ label }: PageLoadingProps) => (
  <div className="page-state" aria-busy="true">
    <p className="page-state__label" role="status">
      {label}
    </p>

    <div className="page-state__skeleton" aria-hidden="true">
      <span className="page-state__bar page-state__bar--title" />
      <div className="page-state__grid">
        {Array.from({ length: 4 }, (_, index) => (
          <span key={index} className="page-state__bar page-state__bar--card" />
        ))}
      </div>
      <span className="page-state__bar page-state__bar--chart" />
    </div>
  </div>
);

type PageErrorProps = {
  title: string;
  message: string;
  onRetry?: () => void;
};

export const PageError = ({ title, message, onRetry }: PageErrorProps) => (
  <div className="page-state page-state--error">
    <h1>{title}</h1>

    <p role="alert">{message}</p>

    {onRetry && (
      <button className="page-state__retry" type="button" onClick={onRetry}>
        Try again
      </button>
    )}
  </div>
);
