import random
import time

from opcua import Server, ua


class MachineSimulator:
    def __init__(self):
        self.scenario = "STOPPED"
        self.tags = {
            "MachineSpeed": 0,
            "ProductionCount": 0,
            "DefectCount": 0,
            "MachineStatus": "STOPPED",
        }
        self.timer = 0
        self.transitions = {
            "PRODUCING": self.on_producing,
            "IDLE": self.on_idle,
            "STARVED": self.on_starved,
            "BLOCKED": self.on_blocked,
            "CHANGEOVER": self.on_changeover,
            "STOPPED": self.on_stopped,
            "FAULTED": self.on_faulted,
        }
        self.server = Server()
        self.server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")
        self.server.start()
        self.add_variables()

    def add_variables(self):
        # Create a new namespace
        uri = "http://examples.freeopcua.github.io"
        idx = self.server.register_namespace(uri)

        # Create a new object in the namespace
        objects = self.server.get_objects_node()
        myobj = objects.add_object(idx, "MyObject")

        # Add variables to the object
        self.speed_var = myobj.add_variable(idx, "MachineSpeed", 0)
        self.production_var = myobj.add_variable(idx, "ProductionCount", 0)
        self.defect_var = myobj.add_variable(idx, "DefectCount", 0)
        self.status_var = myobj.add_variable(idx, "MachineStatus", "STOPPED")

        # Set the variables to be writable by clients
        self.speed_var.set_writable()
        self.production_var.set_writable()
        self.defect_var.set_writable()
        self.status_var.set_writable()

    def simulate(self):
        while True:
            # 初期化
            scenario = self.scenario
            tags = self.tags
            timer = self.timer

            # タイマーチェック
            if timer <= 0:
                next_scenario = self.get_next_scenario(scenario)
                self.scenario = next_scenario
                self.timer = random.randint(5, 15)  # 次の状態までのランダムな時間
            else:
                self.timer -= 1

            # 状態遷移
            if self.scenario in self.transitions:
                self.transitions[self.scenario]()

            # フロー変数の更新
            self.tags = tags
            self.timer = timer

            # OPC UAサーバーの変数を更新
            self.update_opcua_variables()

            print(f"Scenario: {self.scenario}, Tags: {self.tags}, Timer: {self.timer}")
            time.sleep(1)  # 1秒ごとに更新

    def get_next_scenario(self, current_scenario):
        if current_scenario == "STOPPED":
            return "IDLE"
        elif current_scenario == "IDLE":
            return "PRODUCING"
        elif current_scenario == "PRODUCING":
            return random.choice(
                ["IDLE", "STARVED", "BLOCKED", "CHANGEOVER", "FAULTED"]
            )
        elif current_scenario == "STARVED":
            return "PRODUCING"
        elif current_scenario == "BLOCKED":
            return "PRODUCING"
        elif current_scenario == "CHANGEOVER":
            return "PRODUCING"
        elif current_scenario == "FAULTED":
            return "STOPPED"
        return "STOPPED"

    def on_producing(self):
        self.tags["MachineSpeed"] = random.randint(50, 100)
        self.tags["ProductionCount"] += 1
        if random.random() < 0.05:  # 5%の確率で不良品
            self.tags["DefectCount"] += 1
        self.tags["MachineStatus"] = "PRODUCING"

    def on_idle(self):
        self.tags["MachineSpeed"] = 0
        self.tags["MachineStatus"] = "IDLE"

    def on_starved(self):
        self.tags["MachineSpeed"] = 0
        self.tags["MachineStatus"] = "STARVED"

    def on_blocked(self):
        self.tags["MachineSpeed"] = 0
        self.tags["MachineStatus"] = "BLOCKED"

    def on_changeover(self):
        self.tags["MachineSpeed"] = 0
        self.tags["MachineStatus"] = "CHANGEOVER"

    def on_stopped(self):
        self.tags["MachineSpeed"] = 0
        self.tags["MachineStatus"] = "STOPPED"

    def on_faulted(self):
        self.tags["MachineSpeed"] = 0
        self.tags["MachineStatus"] = "FAULTED"

    def update_opcua_variables(self):
        self.speed_var.set_value(self.tags["MachineSpeed"])
        self.production_var.set_value(self.tags["ProductionCount"])
        self.defect_var.set_value(self.tags["DefectCount"])
        self.status_var.set_value(self.tags["MachineStatus"])


if __name__ == "__main__":
    simulator = MachineSimulator()
    try:
        simulator.simulate()
    finally:
        simulator.server.stop()
