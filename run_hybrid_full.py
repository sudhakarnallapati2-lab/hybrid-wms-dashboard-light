import json, os, datetime, random

def main():
    rows=[]
    for ou, backend in [("India_OU","EBS"),("US_OU","SAAS"),("EU_OU","SAAS")]:
        stuck_lpn=random.randint(0,2)
        waves=random.randint(0,1)
        cloud=random.randint(0,3)
        fusion=random.randint(0,2)
        total=stuck_lpn+waves+cloud+fusion
        rows.append({
            "run_time": datetime.datetime.now().isoformat(),
            "ou_name": ou,
            "backend": backend,
            "stuck_lpn": stuck_lpn,
            "aging_waves": waves,
            "cloud_stuck_tasks": cloud,
            "fusion_exceptions": fusion,
            "total_issues": total
        })
    os.makedirs("out", exist_ok=True)
    with open("out/hybrid_report.json","w") as f:
        json.dump(rows,f,indent=2)
    print("✅ Data generated: out/hybrid_report.json")

if __name__=="__main__":
    main()
