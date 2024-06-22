import luigi


class FetchData(luigi.Task):
    def output(self):
        return luigi.LocalTarget('data/fetch_data.txt')

    def run(self):
        with self.output().open('w') as out_file:
            out_file.write('Fetched raw data\n')


class ProcessData(luigi.Task):
    def requires(self):
        return FetchData()

    def output(self):
        return luigi.LocalTarget('data/process_data.txt')

    def run(self):
        with self.input().open('r') as in_file:
            data = in_file.read()
        with self.output().open('w') as out_file:
            out_file.write(f'{data}Processed data\n')


class GenerateReport(luigi.Task):
    def requires(self):
        return [FetchData(), ProcessData()]

    def output(self):
        return luigi.LocalTarget('data/generate_report.txt')

    def run(self):
        fetch_data_content = self.input()[0].open('r').read()
        process_data_content = self.input()[1].open('r').read()

        with self.output().open('w') as out_file:
            out_file.write(
                f'{fetch_data_content}{process_data_content}Generated report\n')


if __name__ == '__main__':
    luigi.build([GenerateReport()], local_scheduler=True)
