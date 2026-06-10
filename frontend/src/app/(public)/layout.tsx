export default function PublicLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <>
      {/* Animated gradient mesh background */}
      <div className="gradient-mesh">
        <div className="mesh-orb-1" />
      </div>

      {/* Page content above the mesh */}
      <div style={{ position: "relative", zIndex: 1, minHeight: "100vh" }}>
        {children}
      </div>
    </>
  );
}
