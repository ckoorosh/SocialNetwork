from social_network import SocialNetwork
from command_processor import CommandProcessor
from block_manager import BlockManager


class Challenge:
    def __init__(self, disk_manager):
        self.dm = disk_manager
        self.network = SocialNetwork(BlockManager(self))
        self.processor = CommandProcessor(self.network)
        self.main_disk = list(self.dm.disks)[0]

    def run(self, events_and_queries):
        for command in events_and_queries:
            self.processor.process(command)
