// src/viewModels/DashboardViewModel.test.ts
import { describe, it, expect } from "vitest";
import { renderHook } from "@testing-library/react";
import { useDashboardViewModel } from "@/viewModels/DashboardViewModel";
import { useAppDispatch, useAppSelector } from "@/store/hooks";
import { fetchAssets } from "../store/modules/assets";
import { fetchTradeDates } from "../store/modules/tradeDates";

// モックの設定
vi.mock("@/store/hooks", () => ({
  useAppDispatch: vi.fn(),
  useAppSelector: vi.fn(),
}));

vi.mock("../store/modules/assets", () => ({
  fetchAssets: vi.fn(),
}));

vi.mock("../store/modules/tradeDates", () => ({
  fetchTradeDates: vi.fn(),
}));

describe("useDashboardViewModel", () => {
  let mockDispatch: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    mockDispatch = vi.fn();
    (useAppDispatch as jest.Mock).mockReturnValue(mockDispatch);
    (useAppSelector as jest.Mock).mockImplementation((selector) =>
      selector({
        auth: { user: { id: "1", name: "Test User" } },
        assets: { assetsData: [], loading: false, error: null },
        tradeDates: { datesData: [], loading: false, error: null },
      })
    );
  });

  it("初期状態が正しく設定されていること", () => {
    const { result } = renderHook(() => useDashboardViewModel());

    expect(result.current.user).toEqual({ id: "1", name: "Test User" });
    expect(result.current.selectedGraphType).toBe("futures-data");
    expect(result.current.selectedAsset).toBe("");
    expect(result.current.selectedTradeDate).toBe("");
    expect(result.current.selectedChart).toBeNull();
  });

  it("コンポーネントマウント時にfetchAssetsが呼ばれること", () => {
    renderHook(() => useDashboardViewModel());

    expect(mockDispatch).toHaveBeenCalledWith(fetchAssets());
  });

  it("selectedAssetが変更されたときにfetchTradeDatesが呼ばれること", async () => {
    const { result } = renderHook(() => useDashboardViewModel());

    // actの代わりに、直接関数を呼び出し、その後の状態変化を待つ
    result.current.setSelectedAsset("BTC");

    // 非同期の状態更新を待つ
    await vi.waitFor(() => {
      expect(mockDispatch).toHaveBeenCalledWith(
        fetchTradeDates({
          graphType: "futures-data",
          asset: "BTC",
        })
      );
    });
  });

  it("setSelectedAssetが正しく動作すること", async () => {
    const { result } = renderHook(() => useDashboardViewModel());

    result.current.setSelectedAsset("BTC");

    await vi.waitFor(() => {
      expect(result.current.selectedAsset).toBe("BTC");
    });
  });

  it("selectChartが正しく動作すること", async () => {
    const { result } = renderHook(() => useDashboardViewModel());

    result.current.selectChart(1);

    await vi.waitFor(() => {
      expect(result.current.selectedChart).toBe(1);
    });
  });

  // 他のテストケースも同様に追加...
});
